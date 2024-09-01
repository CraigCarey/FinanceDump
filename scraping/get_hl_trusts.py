#! /usr/bin/env python3

'''
Compiles a list of InvestmentTrust structs and pickles to file:
    investment_trusts_240901.pkl

and to csv: investment_trusts_240901.csv
'''

from dataclasses import dataclass
import pickle
from datetime import datetime

import pandas as pd

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup


def _get_datestamp():
    now = datetime.now()
    return now.strftime('%y%m%d')


@dataclass
class InvestmentTrust:
    symbol: str
    name: str
    link: str
    tradeable: bool


def check_symbol_row(symbol_row):
    td_rows = symbol_row.findAll('td')

    if len(td_rows) != 4:
        return False

    td_row_1 = td_rows[0].findAll('td')

    return len(td_row_1) == 0


def get_symbol_row_data(symbol_row):
    symbol_rows = symbol_row.findAll('td')
    symbol = symbol_rows[0].text
    name = symbol_rows[1].text
    link = symbol_rows[1].find('a', href=True)['href']
    dealable = symbol_rows[3].text.startswith('\nDeal')

    return symbol, name, link, dealable


def get_page_url(offset):
    url = f'https://www.hl.co.uk/shares/investment-trusts/search-for-investment-trusts?offset={offset}&it_search_input=a&companyid=&sectorid='

    return url


def get_page_urls(soup):
    num_pages = 0

    for link in soup.findAll('a', href=True):
        title = link.get('title')

        if not title:
            continue

        if title.startswith('View page '):
            num_pages += 1

    num_pages = num_pages // 2
    step_size = 50
    max_offset = num_pages * step_size

    page_urls = []
    offset = step_size
    while offset <= max_offset:
        url = get_page_url(offset)
        page_urls.append(url)
        offset += step_size

    return page_urls


def get_inv_trust_data(soup, investment_trusts):
    table = soup.find('table')
    rows = table.find_all('tr')

    for symbol_row in rows:
        if not check_symbol_row(symbol_row):
            continue
        symbol, name, link, dealable = get_symbol_row_data(symbol_row)
        investment_trusts.append(InvestmentTrust(
            symbol, name, link, dealable))


def main():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    url = get_page_url(0)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html')

    page_urls = get_page_urls(soup)

    investment_trusts = []

    get_inv_trust_data(soup, investment_trusts)

    for page_url in page_urls:
        print(page_url)
        driver.get(page_url)
        page_soup = BeautifulSoup(driver.page_source, 'html')

        get_inv_trust_data(page_soup, investment_trusts)

    datestamp = _get_datestamp()

    inv_trusts_filename = f'../data/investment_trusts_{datestamp}.pkl'
    with open(inv_trusts_filename, "wb") as handle:
        pickle.dump(investment_trusts, handle,
                    protocol=pickle.HIGHEST_PROTOCOL)
        
    df = pd.DataFrame([trust.__dict__ for trust in investment_trusts])

    df.to_csv(f'../data/investment_trusts_{datestamp}.csv')


if __name__ == "__main__":
    main()
