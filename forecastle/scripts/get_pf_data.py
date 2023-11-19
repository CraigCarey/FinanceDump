import datetime
import json
import os
import pickle
from pprint import pprint
from time import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fbprophet import Prophet

import yfinance as yf


class ForecastModel:
    def __init__(self, forecast, model):
        self.forecast = forecast
        self.model = model
        self.date = pd.Timestamp.today()


def func_timer(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2 - t1):.4f}s")
        return result

    return wrap_func


@func_timer
def get_ticker_data(ticker: str, refresh: bool = True):
    info_file = f"data/{ticker}.json"
    hist_file = f"data/{ticker}.csv"

    info = None
    history = pd.DataFrame()

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    if os.path.isfile(info_file):
        with open(info_file) as json_info:

            print(f"{info_file} found")
            info = json.load(json_info)

            # Invalidate if stale
            if refresh and info["date"] != today_date:
                print(f"{info_file} stale")
                info = None

    # Only read CSV file if info is valid
    if info and os.path.isfile(hist_file):
        print(f"{hist_file} found")
        history = pd.read_csv(hist_file, index_col="Date")

    if not info or history.empty:
        print(f"Getting data from yfinance: {ticker}")
        yt = yf.Ticker(ticker)
        info = yt.info
        info["date"] = today_date
        history = yt.history(period="2y", interval="1wk")

        if history.empty:
            print(f"WARNING: history of {ticker} is empty, using info")

            try:
                sub_hist = [
                    info["open"],
                    info["dayHigh"],
                    info["dayLow"],
                    info["previousClose"],
                    info["volume"],
                    0.0,
                    0.0,
                ]
            except KeyError:
                sub_hist = [
                    info["regularMarketOpen"],
                    info["regularMarketDayHigh"],
                    info["regularMarketDayLow"],
                    info["regularMarketPreviousClose"],
                    info["regularMarketVolume"],
                    0.0,
                    0.0,
                ]
            history.loc[today_date] = sub_hist

        # Convert currency units
        if info["currency"] == "GBp":
            m = [0.01, 0.01, 0.01, 0.01, 1, 0.01, 1]
            history = history.mul(m)
            info["currency"] = "GBP"
    else:
        print("Reusing cached data")

    if "Returns" not in history:
        history["Returns"] = history["Close"].pct_change()

    cum_rets = ((1 + history["Returns"]).cumprod() - 1)[-1]
    ann_rets = history["Returns"].mean() * 252
    ann_vol = history["Returns"].std() * np.sqrt(252)
    sharpe_ratio = ann_rets / ann_vol

    # Calculate Downside Returns
    sortino_ratio_df = history[["Returns"]].copy()
    sortino_ratio_df.loc[:, "DownsideReturns"] = 0
    target = 0
    mask = sortino_ratio_df["Returns"] < target
    sortino_ratio_df.loc[mask, "DownsideReturns"] = sortino_ratio_df["Returns"] ** 2

    # Calculate Sortino Ratio
    down_stdev = np.sqrt(sortino_ratio_df["DownsideReturns"].mean()) * np.sqrt(252)
    sortino_ratio = ann_rets / down_stdev

    info["Cumulative Returns"] = cum_rets
    info["Annual Returns"] = ann_rets
    info["Annual Volatility"] = ann_vol
    info["Sharpe Ratio"] = sharpe_ratio
    info["Sortino Ratio"] = sortino_ratio

    store_ticker_data(ticker, info, history)

    return info, history


def store_ticker_data(ticker, info, history):
    if not os.path.exists("data"):
        os.makedirs("data")

    # TODO: faster to pickle?
    with open(f"data/{ticker}.json", "w") as json_file:
        json.dump(info, json_file, indent=4)

    history.to_csv(path_or_buf=f"data/{ticker}.csv")


def visualise_ticker(ticker: dict):
    pprint(ticker["info"])

    ticker["history"]["Close"].plot()
    plt.show()


@func_timer
def concat_closes(pf_data: dict) -> pd.DataFrame:
    """
    Constructs a dataframe of all interpolated closings for all holdings
    """
    keys = list(pf_data.keys())
    key_0 = keys[0]
    pf_df = pd.DataFrame(pf_data[key_0]["history"]["Close"])
    pf_df.rename(columns={"Close": key_0}, inplace=True)

    for key in keys[1:]:
        cat_df = pd.DataFrame(pf_data[key]["history"]["Close"])
        cat_df.rename(columns={"Close": key}, inplace=True)
        pf_df = pd.concat([pf_df, cat_df], axis=1)

    return pf_df.interpolate(limit_direction="both")


@func_timer
def calc_wealth(pf_data: dict) -> pd.DataFrame:
    wealth_df = concat_closes(pf_data)
    weights_dict = {d: pf_data[d]["count"] for d in pf_data}

    wealth_df["sum"] = wealth_df.mul(list(weights_dict.values()), axis=1).sum(axis=1)

    return wealth_df


def plot_forecast(forecast, model, title, uncertainty=False):
    fig = model.plot(forecast, xlabel="Date", ylabel="Price", uncertainty=uncertainty)
    fig.suptitle(title)
    fig.show()


@func_timer
def get_forecast(data, period=2):
    ticker = data.columns[0]

    forecast_model = None
    model = None
    forecast = None
    updated = False

    forecast_filename = f"models/{ticker}_forecast.pkl"
    if os.path.isfile(forecast_filename):
        print("Forecast cache found, loading")
        with open(forecast_filename, "rb") as handle:
            forecast_model = pickle.load(handle)
            forecast = forecast_model.forecast
            model = forecast_model.model

    # No previous forecast found, or stored model is out of date
    if forecast_model is None or (pd.Timestamp.now() - forecast_model.date).days > 0:
        # converts the index into a column
        df_train = data.reset_index()
        df_train = df_train.rename(columns={"Date": "ds", ticker: "y"})

        model = Prophet().fit(df_train)

        future = model.make_future_dataframe(periods=period * 365)
        forecast = model.predict(future)
        updated = True

    return forecast, model, updated


@func_timer
def store_forecast(forecast, model, name):
    fc = ForecastModel(forecast, model)
    with open(f"models/{name}_forecast.pkl", "wb") as handle:
        pickle.dump(fc, handle, protocol=pickle.HIGHEST_PROTOCOL)


@func_timer
def generate_forecasts(wealth_pf: pd.DataFrame, plot=True):
    for col in wealth_pf.columns:

        forecast, model, updated = get_forecast(wealth_pf[[col]])

        if plot:
            plot_forecast(forecast, model, col)

        if updated:
            store_forecast(forecast, model, col)


def plot_wealth(wealth_pf):
    wealth_pf.loc[:, wealth_pf.columns.difference(["sum"])].plot(figsize=(15, 8))
    plt.show()

    wealth_pf["sum"].plot(title="wealth")
    plt.show()

    forecast, model, _ = get_forecast(wealth_pf[["sum"]])
    plot_forecast(forecast, model, "wealth")


@func_timer
def get_metrics(pf_data):
    metrics = [
        "Annual Return",
        "Cumulative Returns",
        "Annual Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
    ]
    columns = list(pf_data.keys())

    # Initialize the DataFrame with index set to evaluation metrics
    pf_metrics = pd.DataFrame(index=metrics, columns=columns)

    for k, v in pf_data.items():
        pf_metrics[k] = [
            v["info"]["Cumulative Returns"],
            v["info"]["Annual Returns"],
            v["info"]["Annual Volatility"],
            v["info"]["Sharpe Ratio"],
            v["info"]["Sortino Ratio"],
        ]

    return pf_metrics


@func_timer
def main():
    pf_filename = "portfolio.json"

    if not os.path.isfile(pf_filename):
        raise RuntimeError(f"Can't find portfolio file: {pf_filename}")

    with open(pf_filename) as json_pf:
        pf_data = json.load(json_pf)
        holdings = pf_data["holdings"]

    pf_data = {}

    for holding in holdings:
        ticker = holding["ticker"]
        count = holding["count"]
        info, history = get_ticker_data(ticker, refresh=True)

        pf_data[ticker] = {"info": info, "history": history, "count": count}

    pd.set_option
    pf_metrics = get_metrics(pf_data)
    print(pf_metrics)

    wealth_pf = calc_wealth(pf_data)

    generate_forecasts(wealth_pf)

    plot_wealth(wealth_pf)


if __name__ == "__main__":
    main()
