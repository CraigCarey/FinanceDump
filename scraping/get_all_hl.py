#!/usr/bin/env python3

import re

import requests
from bs4 import BeautifulSoup


def main():

    # market names to num pages
    markets = {
        # "ftse-100": 1,
        # "ftse-250": 3,
        "ftse-350": 4,
        # "ftse-aim-100": 1,
        # "ftse-all-share": 6,
        # "ftse-small-cap": 3,
        # "ftse-techmark-100": 3,
    }

    f_all = open("hl-all-ftse.csv", "w")
    header = "epic, name, current price (p), day change (p), day change (%)\n"
    f_all.write(header)

    for market, pages in markets.items():
        print(f"Scraping {market}...")

        f_market = open(f"{market}.csv", "w")
        f_market.write(header)

        for page in range(1, pages + 1):

            URL = (
                f"https://www.hl.co.uk/shares/stock-market-summary/{market}?page={page}"
            )
            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "html.parser")

            table = soup.find("table", class_="stockTable")

            companies = table.find_all("tr", id=re.compile("ls-row-.*-L"))

            for company_element in companies:

                company_data = company_element.find_all("td")

                row = f"{company_data[0].text.strip()};"
                row += f"{company_data[1].text.strip()};"
                row += f"{company_data[2].text.strip()};"
                row += f"{company_data[3].text.strip()};"
                row += f"{company_data[4].text.strip()}\n"

                f_all.write(row)
                f_market.write(row)


if __name__ == "__main__":
    main()
