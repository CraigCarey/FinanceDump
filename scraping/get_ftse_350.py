#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup


def main():

    URL = "https://www.fidelity.co.uk/shares/ftse-350/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table")

    print(table)

    f = open("ftse350.csv", "w")

    companies = table.find_all("tr")
    for company_element in companies:
        epic = company_element.find("td")

        if epic:
            print(epic.text.strip())
            f.write(f"{epic.text.strip()}\n")


if __name__ == "__main__":
    main()
