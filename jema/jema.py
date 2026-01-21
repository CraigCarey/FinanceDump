#! /usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

from tvdatafeed import TvDatafeed, Interval

import openpyxl

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("future.no_silent_downcasting", True)

shares_in_issue = 40.44e6
declared_nav = 65.9
s_account_divs_feb_rub = 53e6 * 107.9

xlsx_filename = "jpm-emerging-europe-middle-east-afria-disclosure.xlsx"
json_filename = "jema_data.json"
description_col = "Security Description"
security_col = "Security No."
symbol_col = "Symbol"
holding_col = "Holding"
value_col = "Market Value"
percent_col = "% of Fund"
exchange_col = "Exchange"
currency_col = "Currency"
conversion_col = "Conv Rate"
exchange_col = "Exchange"
currency_col = "Currency"
conversion_col = "Conv Rate"
sp_lc_col = "SP LC"
sp_gbp_col = "SP GBP"
holding_gbp_col = "Holding GBP"
nav_gbp_col = "NAV GBP"

tv = TvDatafeed()


def latest_holdings_sheet0_name():
    xls = pd.ExcelFile(xlsx_filename)
    return xls.sheet_names[0]


def generate_month_year_list(start_year, start_month, n_months=36):
    start_month = datetime(year=start_year, month=start_month, day=1)
    month_year_list = []

    for _ in range(n_months):
        # Format the month and year as "Month Year"
        month_year = start_month.strftime("%B %Y")
        month_year_list.append(month_year)

        # Move to the previous month
        # Use timedelta to avoid issues with months of varying lengths
        first_day_of_current_month = start_month.replace(day=1)
        start_month = first_day_of_current_month - timedelta(days=1)

    return month_year_list


def get_jema_holdings_xlsx(outputFile=xlsx_filename):
    local_filename = outputFile
    url = f"https://am.jpmorgan.com/content/dam/jpm-am-aem/emea/gb/en/supplemental/full-portfolio-listing/{xlsx_filename}"

    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Check for HTTP errors

        # Open a local file with write-binary mode
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


def fix_jema_holdings(local_filename=xlsx_filename):
    ss = openpyxl.load_workbook(local_filename)
    ss["Nov 2025"].title = "November 2025"
    ss["Oct 2025"].title = "October 2025"
    ss["Sep 2025"].title = "September 2025"
    ss["Aug 2025"].title = "August 2025"
    ss["Mar 2025"].title = "March 2025"
    ss["Feb 2025"].title = "February 2025"
    ss["Jan 2025"].title = "January 2025"
    ss["Dec 2024"].title = "December 2024"
    ss["Nov 2024"].title = "November 2024"
    ss["Oct 2024"].title = "October 2024"
    ss["Sep 2024"].title = "September 2024"
    ss["Aug 2024"].title = "August 2024"
    ss.save(local_filename)


def get_latest_holdings(local_filename=xlsx_filename):
    month_sheet = latest_holdings_sheet0_name()
    month_data = pd.read_excel(
        local_filename, sheet_name=month_sheet, skiprows=9, usecols=range(5)
    )
    month_data.drop(["% of Fund"], axis=1, inplace=True)
    month_data.dropna(inplace=True)
    month_data = month_data.sort_values(by=description_col).reset_index(drop=True)
    # month_data.to_csv(f"jema_holdings_{month_sheet.replace(' ', '_').lower()}.csv")
    return month_data


def get_symbols_and_exchanges():
    jema_symbols_exchanges = pd.read_csv("./jema_symbols_exchanges.csv").dropna(
        subset=[symbol_col]
    )
    jema_symbols_exchanges.reset_index(inplace=True, drop=True)
    jema_symbols_exchanges = jema_symbols_exchanges.drop(columns=[description_col])
    jema_symbols_exchanges = jema_symbols_exchanges.dropna()
    return jema_symbols_exchanges


def append_symbols_and_exchanges(latest_holdings):
    month_sheet = latest_holdings_sheet0_name()
    symbols_and_exchanges = get_symbols_and_exchanges()
    jema_data = pd.merge(
        latest_holdings, symbols_and_exchanges, on=security_col, how="left"
    )

    jema_data["Conv Rate"] = jema_data["Conv Rate"].fillna(1)
    jema_data = jema_data.fillna("")
    jema_data = jema_data.sort_values(by=[description_col], ignore_index=True)

    cols = [
        description_col,
        security_col,
        symbol_col,
        exchange_col,
        currency_col,
        conversion_col,
        holding_col,
        value_col,
    ]
    jema_data = jema_data[cols]
    jema_data.to_csv("jema_symbols_exchanges_new.csv")
    jema_data.to_csv(f"jema_holdings_{month_sheet.replace(' ', '_').lower()}.csv")

    return jema_data


def get_local_prices(latest_holdings_with_symbols):
    global tv
    failures = []
    consecutive_failures = 0

    if sp_lc_col not in latest_holdings_with_symbols.columns:
        latest_holdings_with_symbols[sp_lc_col] = None

    for index, row in latest_holdings_with_symbols.iterrows():
        symbol = row.Symbol
        exchange = row.Exchange
        sp_lc = row[sp_lc_col]

        if sp_lc is not None:
            continue

        if exchange == "PRIVATE":
            continue

        print(f"Processing: {exchange}:{symbol}")

        try:
            hist = tv.get_hist(
                symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=1
            )

            sp_now = hist.iloc[-1].close.item()
            latest_holdings_with_symbols.loc[index, sp_lc_col] = sp_now
            consecutive_failures = 0
        except Exception as e:
            print(f"Failed: {symbol} - {exchange}")
            failures.append((symbol, exchange))
            consecutive_failures += 1

            if consecutive_failures >= 3:
                print("Resetting connection after 3 consecutive failures...")
                tv = TvDatafeed()
                consecutive_failures = 0

    return failures


def get_fx_rates(latest_holdings_with_symbols):
    currencies = list(latest_holdings_with_symbols[currency_col].unique())

    fx_rates = {}
    for currency in currencies:
        currency = currency.strip()
        currency = currency.upper()
        if currency == "ZAC":
            currency = "ZAR"

        if currency == "KWF":
            currency = "KWD"

        if currency in fx_rates:
            continue
        try:
            data = tv.get_hist(
                symbol=f"{currency}GBP",
                exchange="FX_IDC",
                interval=Interval.in_daily,
                n_bars=100,
            )

            rate = data.iloc[-1].close.item()

            if currency == "ZAR":
                currency = "ZAC"
                rate = rate / 100

            if currency == "KWD":
                currency = "KWF"
                rate = rate / 1000

            fx_rates[currency] = rate
        except:
            print(f"Failed: {currency}GBP")

    return fx_rates


def apply_rates(latest_holdings_with_symbols, fx_rates):
    for index, row in latest_holdings_with_symbols.iterrows():

        if row[exchange_col] == "PRIVATE":
            continue

        currency = row[currency_col]
        fx_rate = fx_rates[currency]
        sp_lc = row[sp_lc_col]
        sp_gbp = sp_lc * fx_rate
        latest_holdings_with_symbols.loc[index, sp_gbp_col] = sp_gbp
        holding = row[holding_col]

        latest_holdings_with_symbols.loc[index, holding_gbp_col] = holding * sp_gbp


def get_price(symbol, exchange):
    sp = 0
    try:
        hist = tv.get_hist(
            symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=1
        )

        sp = hist.iloc[-1].close.item()
    except:
        print(f"Failed: {symbol} - {exchange}")
    return sp


def create_jema_json(latest_holdings_with_symbols, fx_rates):
    s_account_divs_now_gbp = int(s_account_divs_feb_rub * fx_rates["RUB"])
    s_account_divs_per_share = s_account_divs_now_gbp / shares_in_issue

    total_holding_gbp = int(latest_holdings_with_symbols[holding_gbp_col].sum())
    total_holding_rus = int(
        latest_holdings_with_symbols[latest_holdings_with_symbols["Currency"] == "RUB"][
            holding_gbp_col
        ].sum()
    )
    total_holding_non = total_holding_gbp - total_holding_rus

    equity_nav_gbp = total_holding_gbp / shares_in_issue
    total_nav_gbp = equity_nav_gbp + s_account_divs_per_share

    jema_price = get_price("JEMA", "LSE") / 100
    official_pd = -(1 - (jema_price / (declared_nav / 100)))
    equity_pd_total = -(1 - (jema_price / equity_nav_gbp))
    actual_pd_total = -(1 - (jema_price / total_nav_gbp))

    # print(f"{int(total_holding_gbp):,}")
    # print(f"{equity_nav_gbp:.2f} GBP per share")
    # print(f"JEMA price: {jema_price:.2f} GBP")
    # print(f"S Account Divs: {s_account_divs_now_gbp:,}")
    # print(f"S account divs per share: {s_account_divs_per_share:.2f}")
    # print(f"Total NAV: {total_nav_gbp:.2f}")

    # print(f"Total Russian Holding: {total_holding_rus:,}")
    # print(f"Total Non-Russian Holding: {total_holding_non:,}")
    # print(f"Total holdings: {total_holding_gbp:,}")

    data_to_write = {
        "total_holding_gbp": total_holding_gbp,
        "equity_nav_gbp": equity_nav_gbp,
        "jema_price": jema_price,
        "s_account_divs_now_gbp": s_account_divs_now_gbp,
        "s_account_divs_per_share": s_account_divs_per_share,
        "total_nav_gbp": total_nav_gbp,
        "total_holding_rus": total_holding_rus,
        "total_holding_non": total_holding_non,
        "data_timestamp": datetime.now().isoformat(),
        "declared_nav": declared_nav,
        "official_pd": official_pd,
        "equity_pd_total": equity_pd_total,
        "actual_pd_total": actual_pd_total,
    }

    with open(json_filename, "w") as json_file:
        json.dump(data_to_write, json_file, indent=4)


def read_jema_json():
    with open(json_filename, "r") as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    # get_jema_holdings_xlsx()
    # fix_jema_holdings()
    latest_holdings = get_latest_holdings()
    latest_holdings_with_symbols = append_symbols_and_exchanges(latest_holdings)
    print(latest_holdings_with_symbols)
