#! /usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup

def selenium_method():

    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    url = 'https://www.hl.co.uk/shares/investment-trusts/search-for-investment-trusts?offset=0&it_search_input=a&companyid=&sectorid='
    driver.get(url)

    elements = driver.find_elements(By.CLASS_NAME, '-dataCell')

    for element in elements:
        print (element)

    driver.quit()

def bs_method():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    url = 'https://www.hl.co.uk/shares/investment-trusts/search-for-investment-trusts?offset=0&it_search_input=a&companyid=&sectorid='
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    # symbol = soup.find('td')

    # print(author_element.text)

    # Find the table element
    table = soup.find('table')

    # print(table)

    # Create a list to store the parsed data
    data = []

    # Iterate over the table rows
    rows = table.find_all('tr')
    for row in table.find_all('tr'):

        print(row)
        print()

        # Create a dictionary to store the row data
        row_data = {}

        # Iterate over the table columns
        for column in row.find_all('td'):

            print(column)

            # Extract the column header
            column_header = column.get('class')[0]

            # Extract the column value
            column_value = column.text

            # Add the column header and value to the row data dictionary
            row_data[column_header] = column_value

        print(row_data)

        break

        # Add the row data dictionary to the data list
        data.append(row_data)

    # # Print the parsed data
    # print(data)

    driver.quit()

bs_method()

# print()

# soup = BeautifulSoup(driver.page_source, 'lxml')
# author_element = soup.find('small', class_='author')

# print(author_element.text)

# driver.quit()
