#! /usr/bin/env python3

import pickle

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup

import pandas as pd

from dataclasses import dataclass

import datetime

from investment_trust import InvestmentTrust

@dataclass
class TrustData:
    nav: str
    nav_premium: str
    volume: str
    div_yld: str
    annual_mgmt_charge: str
    performance_fee: str
    ongoing_charge: str
    total_assets: str
    gross_gearing: str
    market_cap: str
    structure: str
    domicile: str
    isin: str
    objective: str


def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%y%m%d_%H%M%S')

def get_sec_detail(soup, idx):
    sec_det = soup.find(id='security-detail')
    return sec_det.find_all('strong')[idx].text

def get_trust_basics(soup, idx):
    trust_basics = soup.find_all(class_='factsheet-table table-no-border spacer-bottom')[0]
    return trust_basics.find_all('td')[idx].text.replace('\n', '').replace('\t', '')

def get_objective(soup):
    return soup.find_all("div", class_="grey-gradient clearfix")[1].text.replace('\n', '').replace('\t', '')

def get_symbol_data(soup):

    idx_nav_premium = 7
    idx_nav = 3
    idx_volume = 8
    idx_div_yld = 9

    annual_mgmt_charge_idx = 1
    performance_fee_idx = 2
    ongoing_charge_idx = 3
    total_assets_idx = 6
    gross_gearing_idx = 7
    market_cap_idx = 8
    structure_idx = 10
    domicile_idx = 11
    isin_idx = 12

    nav = get_sec_detail(soup, idx_nav)
    nav_premium = get_sec_detail(soup, idx_nav_premium)
    volume = get_sec_detail(soup, idx_volume)
    div_yld = get_sec_detail(soup, idx_div_yld)

    annual_mgmt_charge = get_trust_basics(soup, annual_mgmt_charge_idx).replace(' ', '')
    performance_fee = get_trust_basics(soup, performance_fee_idx).replace(' ', '')
    ongoing_charge = get_trust_basics(soup, ongoing_charge_idx).replace(' ', '')
    total_assets = get_trust_basics(soup, total_assets_idx).replace(' ', '')
    gross_gearing = get_trust_basics(soup, gross_gearing_idx).replace(' ', '')
    market_cap = get_trust_basics(soup, market_cap_idx).replace(' ', '')
    structure = get_trust_basics(soup, structure_idx)
    domicile = get_trust_basics(soup, domicile_idx)
    isin = get_trust_basics(soup, isin_idx)

    objective = get_objective(soup)

    trust_data = TrustData(nav, nav_premium, volume, div_yld, annual_mgmt_charge, performance_fee, ongoing_charge, total_assets, gross_gearing, market_cap, structure, domicile, isin, objective)

    return trust_data


def main():

    inv_trusts_filename = '../data/investment_trusts_231002b.pkl'
    with open(inv_trusts_filename, "rb") as handle:
        investment_trusts = pickle.load(handle)

    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    df_columns = ['symbol', 'name', 'nav', 'nav_premium', 'volume', 'div_yld', 'annual_mgmt_charge', 'performance_fee', 'ongoing_charge', 'total_assets', 'gross_gearing', 'market_cap', 'structure', 'domicile', 'isin', 'objective', 'link']
    df = pd.DataFrame(columns=df_columns)

    timestamp = get_timestamp()
    
    for trust in investment_trusts:
        
        if not trust.tradeable:
            print(f"{trust.name} not tradeable")
            continue

        print(f"{trust.name}")

        url = trust.link

        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            trust_data = get_symbol_data(soup)

            trust_dict = {
                'symbol': trust.symbol,
                'name': trust.name,
                'nav': trust_data.nav,
                'nav_premium': trust_data.nav_premium,
                'volume': trust_data.volume,
                'div_yld': trust_data.div_yld,
                'annual_mgmt_charge': trust_data.annual_mgmt_charge,
                'performance_fee': trust_data.performance_fee,
                'ongoing_charge': trust_data.ongoing_charge,
                'total_assets': trust_data.total_assets,
                'gross_gearing': trust_data.gross_gearing,
                'market_cap': trust_data.market_cap,
                'structure': trust_data.structure,
                'domicile': trust_data.domicile,
                'isin': trust_data.isin,
                'objective': trust_data.objective,
                'link': trust.link
            }

            df2 = pd.DataFrame(trust_dict, index=[0])
            df = pd.concat([df2, df], ignore_index=True)
            
            inv_trusts_nav_filename = f'investment_trusts_with_nav_{timestamp}_tmp.pkl'
            with open(inv_trusts_nav_filename, "wb") as handle:
                pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

        except:
            print(f"{trust.name} failed")
            
    inv_trusts_nav_filename = f'investment_trusts_with_nav_{timestamp}.pkl'
    with open(inv_trusts_nav_filename, "wb") as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

    df.to_csv(path_or_buf=f"trusts.csv")


if __name__ == "__main__":
    main()
