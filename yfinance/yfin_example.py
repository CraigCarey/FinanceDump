#!/usr/bin/env python3

from pprint import pprint

import pandas as pd
import yahoo_fin.stock_info as si

import yfinance as yf


def main():

    msft = yf.Ticker("MSFT")  # using yfinance
    msft_data = si.get_quote_table("MSFT")  # using yahoo_fin

    # get stock info
    msft.info

    # get info keys
    info_keys = list(msft.info.keys())
    info_keys.sort()

    pprint(info_keys)

    # convert info to dataframe
    df = pd.DataFrame.from_dict(msft.info, orient="index")
    df = df.reset_index()

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    print(df)

    # EPS from yahoo_fin
    msft_data["EPS (TTM)"]

    # get historical market data
    hist = msft.history(period="max")

    # show actions (dividends, splits)
    msft.actions

    # show dividends
    msft.dividends

    # show splits
    msft.splits

    # show financials
    msft.financials
    msft.quarterly_financials

    # show major holders
    msft.major_holders

    # show institutional holders
    msft.institutional_holders

    # show balance sheet
    msft.balance_sheet
    msft.quarterly_balance_sheet

    # show cashflow
    msft.cashflow
    msft.quarterly_cashflow

    # show earnings
    msft.earnings
    msft.quarterly_earnings

    # show sustainability
    msft.sustainability

    # show analysts recommendations
    msft.recommendations

    # show next event (earnings, etc)
    msft.calendar

    # show all earnings dates
    msft.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    msft.isin

    # show options expirations
    msft.options

    # show news
    msft.news

    # get option chain for specific expiration
    opt = msft.option_chain("YYYY-MM-DD")
    # data available via: opt.calls, opt.puts


if __name__ == "__main__":
    main()
