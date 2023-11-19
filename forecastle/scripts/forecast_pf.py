import json
import os.path
import pickle
from datetime import date, datetime

import pandas as pd
from fbprophet import Prophet
from plotly import graph_objs as go

import yfinance as yf

START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
FORECAST_YRS = 5


def load_data(ticker: str) -> pd.DataFrame:
    """
    Requests ticker data from the yfinance API

    :param ticker: Name of the ticker to obtain data for
    :type ticker: str
    :return: Time series data of ticker prices
    :rtype: pd.Dataframe
    """
    ticker_data = yf.download(ticker, START, TODAY)

    # put date in 1st column
    ticker_data.reset_index(inplace=True)

    return ticker_data


def plot_raw_data(ticker_name, ticker_data, show=False):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=ticker_data["Date"], y=ticker_data["Open"], name="stock_open")
    )
    fig.add_trace(
        go.Scatter(x=ticker_data["Date"], y=ticker_data["Close"], name="stock_close")
    )
    fig.layout.update(
        title_text=f"Time series data {ticker_name}", xaxis_rangeslider_visible=True
    )

    if show:
        fig.show()


def plot_forecast(ticker_name, forecast, show=False):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["trend"], name="price"))
    fig.layout.update(
        title_text=f"Time series data {ticker_name}", xaxis_rangeslider_visible=True
    )

    if show:
        fig.show()


def get_forecast(data, period):
    df_train = data[["Date", "Close"]]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    model = Prophet()
    model.fit(df_train)

    future = model.make_future_dataframe(periods=period * 365)
    forecast = model.predict(future)

    return forecast, model


def aggregate_forecasts(forecasts: dict, holdings: dict):
    """
    Scales each forecast according to the size of the size of the holding, and
    accumulates
    :param forecasts:
    :type forecasts:
    :param holdings:
    :type holdings:
    :return:
    :rtype:
    """
    agg_forecast = None

    for holding in holdings:
        forecast = forecasts[holding["ticker"]]["forecast"]
        # forecast = forecast["forecast"].tail(FORECAST_YRS * 365)
        # forecast = forecast.reset_index()
        forecast["trend"] = forecast["trend"] * holding["count"]

        if agg_forecast is None:
            agg_forecast = forecast
        else:
            agg_forecast["trend"].add(forecast["trend"])

    # TODO
    # agg_forecast = agg_forecast.interpolate()

    return agg_forecast


def main():
    pf_filename = "portfolio.json"

    if not os.path.isfile(pf_filename):
        raise RuntimeError(f"Can't find portfolio file: {pf_filename}")

    with open(pf_filename) as json_pf:
        pf_data = json.load(json_pf)
        holdings = pf_data["holdings"]

    prices_filename = "prices_ts.pkl"
    forecasts_filename = "forecasts.pkl"

    prices_ts_data = {}
    forecasts = {}

    if os.path.isfile(prices_filename):
        print("Prices data cache found, loading")
        with open(prices_filename, "rb") as handle:
            prices_ts_data = pickle.load(handle)

    if os.path.isfile(forecasts_filename):
        print("Forecasts data cache found, loading")
        with open(forecasts_filename, "rb") as handle:
            forecasts = pickle.load(handle)

    prices_updated = False
    forecasts_updated = False

    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)

    for holding in holdings:
        ticker_name = holding["ticker"]
        if ticker_name in prices_ts_data:
            ticker_data = prices_ts_data[ticker_name]["price_ts"]
        else:
            print(f"{ticker_name} not found in prices cache, requesting...")
            ticker_data = load_data(ticker_name)
            prices_ts_data[ticker_name] = {
                "timestamp": int(datetime.utcnow().timestamp()),
                "price_ts": ticker_data,
            }
            prices_updated = True

        plot_raw_data(ticker_name, ticker_data, show=False)

        if ticker_name in forecasts:
            forecast = forecasts[ticker_name]["forecast"]
            model = forecasts[ticker_name]["model"]
        else:
            print(f"{ticker_name} not found in forecasts cache, generating...")
            forecast, model = get_forecast(ticker_data, FORECAST_YRS)
            forecasts[ticker_name] = {
                "timestamp": int(datetime.utcnow().timestamp()),
                "forecast": forecast,
                "model": model,
            }
            forecasts_updated = True

        print("historical:\n", ticker_data)
        print("forecast:\n", forecast)

        # fig1 = plot_plotly(model, forecast)
        # fig1.show()

    pf_aggregate = aggregate_forecasts(forecasts, holdings)

    plot_forecast("aggr", pf_aggregate, True)

    if prices_updated:
        with open(prices_filename, "wb") as handle:
            pickle.dump(prices_ts_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if forecasts_updated:
        with open(forecasts_filename, "wb") as handle:
            pickle.dump(forecasts, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
