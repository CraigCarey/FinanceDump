#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime
import re

import pandas as pd

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup

from tenacity import retry, stop_after_attempt, wait_exponential

# pd.set_option("future.no_silent_downcasting", True)

data_dir = "./data"
datestamp = datetime.now().strftime("%y%m%d")
max_retries = 5

options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


@dataclass
class InvestmentTrust:
    symbol: str
    name: str
    link: str
    tradeable: bool


@dataclass
class TrustData:
    symbol: str = ""
    name: str = ""
    estimate_nav: float = 0
    latest_actual_nav: float = 0
    latest_actual_nav_date: str = ""
    nav_premium: str = ""
    average_12_month_nav_premium: str = ""
    nav_frequency: str = ""
    volume: float = 0
    div_yld: str = ""
    currency: str = ""
    annual_mgmt_charge: str = ""
    performance_fee: bool = False
    ongoing_charge: str = ""
    total_assets_mils: float = 0
    gross_gearing: str = ""
    market_cap_mils: float = 0
    structure: str = ""
    domicile: str = ""
    isin: str = ""
    objective: str = ""
    top_ten_holdings: List[Tuple[str, str]] = field(default_factory=list)
    top_ten_sectors: List[Tuple[str, str]] = field(default_factory=list)
    top_ten_countries: List[Tuple[str, str]] = field(default_factory=list)
    tradeable: bool = False
    link: str = ""
    # winding_down: bool = False
    # auditable: bool = False
    # audit_link: str = ""


def check_symbol_row(symbol_row):
    td_rows = symbol_row.findAll("td")

    if len(td_rows) != 4:
        return False

    td_row_1 = td_rows[0].findAll("td")

    return len(td_row_1) == 0


def get_symbol_row_data(symbol_row):
    symbol_rows = symbol_row.findAll("td")
    symbol = symbol_rows[0].text
    name = symbol_rows[1].text
    link = symbol_rows[1].find("a", href=True)["href"]
    dealable = symbol_rows[3].text.startswith("\nDeal")

    return symbol, name, link, dealable


def get_page_url(offset, search_input):
    url = f"https://www.hl.co.uk/shares/investment-trusts/search-for-investment-trusts?offset={offset}&it_search_input={search_input}"

    return url


def get_page_urls(soup, search_input):
    num_pages = 0

    for link in soup.findAll("a", href=True):
        title = link.get("title")

        if not title:
            continue

        if title.startswith("View page "):
            num_pages += 1

    num_pages = num_pages // 2
    step_size = 50
    max_offset = num_pages * step_size

    page_urls = []
    offset = step_size
    while offset <= max_offset:
        url = get_page_url(offset, search_input)
        page_urls.append(url)
        offset += step_size

    return page_urls


def get_inv_trust_data(soup, investment_trusts):
    table = soup.find("table")
    rows = table.find_all("tr")

    for symbol_row in rows:
        if not check_symbol_row(symbol_row):
            continue

        symbol, name, link, dealable = get_symbol_row_data(symbol_row)

        found_sym = next(
            (trust for trust in investment_trusts if trust.symbol == symbol), None
        )

        if not found_sym:
            investment_trusts.append(
                InvestmentTrust(symbol, name, link, dealable))


def get_trusts():
    # most frequent letters, give us 351, 374 then 375 results
    search_inputs = ["e", "a", "r"]
    investment_trusts = []

    for search_input in search_inputs:

        # Get page 1, so we can determine how many other pages there are
        url = get_page_url(0, search_input)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "lxml")

        # Scrape the first page
        get_inv_trust_data(soup, investment_trusts)

        # Generate URLs for the other pages
        page_urls = get_page_urls(soup, search_input)

        # Scrape the other pages
        for page_url in page_urls:
            print(page_url)
            driver.get(page_url)
            soup = BeautifulSoup(driver.page_source, "lxml")

            get_inv_trust_data(soup, investment_trusts)

        print(f"num trusts: {len(investment_trusts)}")

    df = pd.DataFrame([trust.__dict__ for trust in investment_trusts])

    df.to_csv(f"{data_dir}/investment_trusts_{datestamp}.csv")

    return df


def convert_to_bool(value):
    if value == "Yes":
        return True
    elif value == "No":
        return False
    else:
        return None


def convert_currency_to_float_mils(value):
    # Remove currency symbols, leave decimal point and multiplier
    numeric_value = re.sub(r"[^\d\.kmb]", "", value.lower())

    # Check for 'k' (thousand), 'm' (millions) or 'b' (billions) and convert accordingly
    if "k" in numeric_value:
        return float(numeric_value.replace("k", "")) / 1_000
    elif "m" in numeric_value:
        return float(numeric_value.replace("m", ""))
    elif "b" in numeric_value:
        return float(numeric_value.replace("b", "")) * 1_000
    else:
        return float(numeric_value)


def get_sec_detail(soup, idx):
    sec_det = soup.find(id="security-detail")
    return sec_det.find_all("strong")[idx].text


def get_trust_basics(soup, idx):
    trust_basics = soup.find_all(
        class_="factsheet-table table-no-border spacer-bottom"
    )[0]
    return trust_basics.find_all("td")[idx].text.replace("\n", "").replace("\t", "")


def get_nav_data(soup, idx):
    nav_table = soup.find_all(
        class_="factsheet-table table-no-border spacer-bottom")[1]
    return nav_table.find_all("td")[idx].text.replace("\n", "").replace("\t", "")


def get_objective(soup):
    return (
        soup.find_all("div", class_="grey-gradient clearfix")[1]
        .text.replace("\n", "")
        .replace("\t", "")
    )


def get_top_ten(soup, divID):
    div = soup.find("div", id=divID)

    top_ten_data = []

    if div:
        table = div.find("table")
        if table:
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                category = columns[0].get_text(strip=True)
                weight = columns[1].get_text(strip=True)
                top_ten_data.append((category, weight))

    return top_ten_data


def get_dummy_symbol_data(trust: InvestmentTrust) -> TrustData:
    trust_data = TrustData()
    trust_data.symbol = trust.symbol
    trust_data.name = trust.name
    trust_data.link = trust.link
    trust_data.tradeable = trust.tradeable

    return trust_data


@retry(
    stop=stop_after_attempt(max_retries),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
def get_symbol_data(trust) -> TrustData:

    url = trust.link
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    idx_volume = 8
    idx_div_yld = 9
    idx_currency = 10

    idx_estimate_nav = 0
    idx_actual_nav = 1
    idx_actual_nav_date = 2
    idx_nav_premium = 3
    idx_average_12_month_nav_premium = 4
    idx_nav_frequency = 5

    idx_annual_mgmt_charge = 1
    idx_performance_fee = 2
    idx_ongoing_charge = 3
    idx_total_assets = 6
    idx_gross_gearing = 7
    idx_market_cap = 8
    idx_structure = 10
    idx_domicile = 11
    idx_isin = 12

    volume = get_sec_detail(soup, idx_volume)
    div_yld = get_sec_detail(soup, idx_div_yld)
    currency = get_sec_detail(soup, idx_currency).strip()

    estimate_nav = re.sub(r"[^\d.]", "", get_nav_data(soup, idx_estimate_nav))
    latest_actual_nav = re.sub(
        r"[^\d.]", "", get_nav_data(soup, idx_actual_nav))
    latest_actual_nav_date = get_nav_data(soup, idx_actual_nav_date)
    nav_premium = get_nav_data(soup, idx_nav_premium)
    average_12_month_nav_premium = get_nav_data(
        soup, idx_average_12_month_nav_premium)
    nav_frequency = get_nav_data(soup, idx_nav_frequency)

    annual_mgmt_charge = get_trust_basics(soup, idx_annual_mgmt_charge).strip()
    performance_fee = get_trust_basics(soup, idx_performance_fee).strip()
    ongoing_charge = get_trust_basics(soup, idx_ongoing_charge).strip()
    total_assets = get_trust_basics(soup, idx_total_assets).strip()
    total_assets_mils = convert_currency_to_float_mils(total_assets)
    gross_gearing = get_trust_basics(soup, idx_gross_gearing).strip()
    market_cap = get_trust_basics(soup, idx_market_cap).strip()
    market_cap_mils = convert_currency_to_float_mils(market_cap)
    structure = get_trust_basics(soup, idx_structure)
    domicile = get_trust_basics(soup, idx_domicile)
    isin = get_trust_basics(soup, idx_isin)

    objective = get_objective(soup)

    top_ten_holdings = get_top_ten(soup, "top-exposures")
    top_ten_sectors = get_top_ten(soup, "top-sectors")
    top_ten_countries = get_top_ten(soup, "top-countries")

    trust_data = TrustData(
        symbol=trust.symbol,
        name=trust.name,
        estimate_nav=estimate_nav,
        latest_actual_nav=latest_actual_nav,
        latest_actual_nav_date=latest_actual_nav_date,
        nav_premium=nav_premium,
        average_12_month_nav_premium=average_12_month_nav_premium,
        nav_frequency=nav_frequency,
        volume=volume,
        div_yld=div_yld,
        currency=currency,
        annual_mgmt_charge=annual_mgmt_charge,
        performance_fee=convert_to_bool(performance_fee),
        ongoing_charge=ongoing_charge,
        total_assets_mils=total_assets_mils,
        gross_gearing=gross_gearing,
        market_cap_mils=market_cap_mils,
        structure=structure,
        domicile=domicile,
        isin=isin,
        objective=objective,
        top_ten_holdings=top_ten_holdings,
        top_ten_sectors=top_ten_sectors,
        top_ten_countries=top_ten_countries,
        tradeable=trust.tradeable,
        link=trust.link,
    )

    return trust_data


def get_trust_data(investment_trusts):
    # investment_trusts.drop(["Unnamed: 0"], axis=1).reset_index(drop=True)

    trusts = []
    num_trusts = len(investment_trusts)
    for trust in investment_trusts.itertuples():

        print(f"[{trust.Index} / {num_trusts}] {trust.name}")

        try:
            trusts.append(get_symbol_data(trust))
        except:
            print(f"{trust.name} FAILED")
            failed_trust = TrustData(
                symbol=trust.symbol,
                name=trust.name,
                tradeable=trust.tradeable,
                link=trust.link,
            )
            trusts.append(failed_trust)

    df = pd.DataFrame([trust.__dict__ for trust in trusts])
    df["div_yld"] = df["div_yld"].replace("n/a", "0%")
    df["volume"] = df["volume"].replace("n/a", "0")
    df["latest_actual_nav"] = df["latest_actual_nav"].replace("n/a", "0")
    df["annual_mgmt_charge"] = df["annual_mgmt_charge"].replace("n/a", "0%")

    inv_trusts_nav_filename = f"{data_dir}/investment_trust_data_{datestamp}.csv"

    df.to_csv(path_or_buf=inv_trusts_nav_filename)

    print(f"Wrote trust data to {inv_trusts_nav_filename}")


def get_audit_df():
    audit_data_filename = f"{data_dir}/investment_trust_data_audit.csv"

    audit_df = pd.read_csv(audit_data_filename).drop(["isin"], axis=1)
    audit_df["winding_down"] = audit_df["winding_down"].fillna(False)
    # audit_df['auditable'] = audit_df['auditable'].fillna(False)
    audit_df["audit_link"] = audit_df["audit_link"].fillna("")

    return audit_df


def augment_data(df):
    audit_df = get_audit_df()
    trusts_with_audit = pd.merge(df, audit_df, on="symbol", how="inner")
    trusts_with_audit.to_csv(
        f"{data_dir}/investment_trust_data_audit_{datestamp}.csv")


def main():
    df = get_trusts()

    # inv_trusts_filename = f"{data_dir}/investment_trusts_{datestamp}.csv"
    # df = (
    #     pd.read_csv(inv_trusts_filename)
    #     .drop(["Unnamed: 0"], axis=1)
    #     .reset_index(drop=True)
    # )

    get_trust_data(df)

    # inv_trusts_filename = f"{data_dir}/investment_trust_data_{datestamp}.csv"
    # df = pd.read_csv(inv_trusts_filename)

    augment_data(df)


if __name__ == "__main__":
    main()
