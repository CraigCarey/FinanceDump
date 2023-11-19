#! /usr/bin/env python3

# Oxylabs - Scraping Dynamic JavaScript Websites - Beautiful Soup Python
# https://youtu.be/Xz514u4V_ts?si=Wbo89TTxSHrJ2fgS

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

from bs4 import BeautifulSoup

options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get('https://quotes.toscrape.com/js')

# <small class="author">Albert Einstein</small>
# selenium-python.readthedocs.io/locating-elements.html
# element = driver.find_element(By.TAG_NAME, 'small')
element = driver.find_element(By.CLASS_NAME, 'author')
print (element.text)

elements = driver.find_elements(By.CLASS_NAME, 'author')

for element in elements:
    print (element.text)

print()

soup = BeautifulSoup(driver.page_source, 'lxml')
author_element = soup.find('small', class_='author')

print(author_element.text)

driver.quit()
