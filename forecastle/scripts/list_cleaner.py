#!/usr/bin/env python

import csv
import datetime
import json
import os

import yfinance as yf


def clean_csv(index: str):
    char1 = "("
    char2 = ")"
    ticker_codes = []
    with open(f"tickers/{index}.csv", mode="r") as csv_file:
        reader = csv.reader(csv_file)

        for item in reader:
            i0 = item[0]
            ticker_code = i0[i0.find(char1) + 1 : i0.find(char2)]
            ticker_codes.append(ticker_code)
    with open(f"tickers/{index}_cleaned.csv", mode="w") as csv_file:
        for tc in ticker_codes:
            csv_file.write(f"{tc}.L\n")


def check_csv(index: str):
    with open(f"tickers/{index}_cleaned.csv", mode="r") as csv_file:
        reader = csv.reader(csv_file)
        for item in reader:
            ticker_code = item[0]
            print(f"checking {ticker_code}")

            info_file = f"data/{ticker_code}.json"

            if os.path.isfile(info_file):
                continue

            yt = yf.Ticker(ticker_code)
            info = yt.info
            if not info["regularMarketPrice"]:
                print(f"{ticker_code} not found")
                continue

            today_date = datetime.datetime.now().strftime("%x")
            info["date"] = today_date
            with open(f"data/{ticker_code}.json", "w") as json_file:
                json.dump(info, json_file, indent=4)


# clean_csv('ftse250')
check_csv("ftse250")
