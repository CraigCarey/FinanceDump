#!/usr/bin/env python3

import re

import requests
from bs4 import BeautifulSoup


def main():

    f = open("ftse_all_share.csv", "w")
    header = "epic, name, current price (p), day change (p), day change (%)\n"
    f.write(header)

    for page in range(1, 7):
        URL = f"https://www.hl.co.uk/shares/stock-market-summary/ftse-all-share?page={page}"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        table = soup.find("table", class_="stockTable")

        companies = table.find_all("tr", id=re.compile("ls-row-.*-L"))

        for company_element in companies:

            company_data = company_element.find_all("td")

            row = f"{company_data[0].text.strip()},"
            row += f"{company_data[1].text.strip()},"
            row += f"{company_data[2].text.strip()},"
            row += f"{company_data[3].text.strip()},"
            row += f"{company_data[4].text.strip()}\n"

            f.write(row)


if __name__ == "__main__":
    main()
