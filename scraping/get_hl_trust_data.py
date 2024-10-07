#! /usr/bin/env python3

from typing import List, Tuple
from datetime import datetime
from dataclasses import dataclass, field
import re

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ChromeOptions

import pandas as pd

from tenacity import retry, stop_after_attempt, wait_exponential

from investment_trust import InvestmentTrust

max_retries = 5

options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


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
    nav_table = soup.find_all(class_="factsheet-table table-no-border spacer-bottom")[1]
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
    latest_actual_nav = re.sub(r"[^\d.]", "", get_nav_data(soup, idx_actual_nav))
    latest_actual_nav_date = get_nav_data(soup, idx_actual_nav_date)
    nav_premium = get_nav_data(soup, idx_nav_premium)
    average_12_month_nav_premium = get_nav_data(soup, idx_average_12_month_nav_premium)
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


def main():

    datestamp = datetime.now().strftime("%y%m%d")
    inv_trusts_filename = f"../data/investment_trusts_{datestamp}.csv"
    investment_trusts = (
        pd.read_csv(inv_trusts_filename)
        .drop(["Unnamed: 0"], axis=1)
        .reset_index(drop=True)
    )

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

    inv_trusts_nav_filename = f"../data/investment_trust_data_{datestamp}.csv"
    # with open(f"{inv_trusts_nav_filename}.pkl", "wb") as handle:
    #     pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

    df.to_csv(path_or_buf=inv_trusts_nav_filename)

    print(f"Wrote trust data to {inv_trusts_nav_filename}")

    # with open(f"{inv_trusts_nav_filename}_failed.txt", "w") as file:
    #     for failure in failures:
    #         file.write(failure + "\n")

    # print(f"Wrote failed trusts to {inv_trusts_nav_filename}_failed.txt")


if __name__ == "__main__":
    main()
