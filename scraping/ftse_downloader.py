#!/usr/bin/env python3

import pickle

import pandas as pd

import yfinance as yf

ticker_files = [
    "ftse-100",
    "ftse-250",
    "ftse-350",
    "ftse-aim-100",
    "ftse-all-share",
    "ftse-small-cap",
    "ftse-techmark-100",
    "hl-all-ftse",
]

pkl_file = "all_ftse_221210.pkl"


def main():
    ticker_symbols = []

    for f in ticker_files:
        print(f"reading {f}.csv")
        df = pd.read_csv(f"{f}.csv")
        print(df)
        df_tickers = df["epic"].tolist()
        print(df_tickers)
        exit(0)
        ticker_symbols.extend(df_tickers)

    ticker_symbols = sorted(set(ticker_symbols))
    print("Number after cleaning:", len(ticker_symbols))

    print(ticker_symbols)
    exit(0)

    file = open("all_ftse_221210.pkl", "rb")
    tickers_dict = pickle.load(file)

    print(type(tickers_dict))
    print(len(tickers_dict))

    for ticker_symbol in ticker_symbols:
        print(ticker_symbol)
        if "BT.A" in ticker_symbol:
            ticker_symbol = "BT-A.L"
        elif "." in ticker_symbol:
            ticker_symbol += "L"
        else:
            ticker_symbol += ".L"

        if ticker_symbol not in tickers_dict:
            print(f"need {ticker_symbol}")
            # ticker = yf.Ticker(ticker_symbol)
            # if ('symbol' not in ticker.info):
            #     print(f"Failed to get data for {ticker_symbol}")
            #     continue
            # tickers_dict[ticker_symbol] = ticker


if __name__ == "__main__":
    main()
