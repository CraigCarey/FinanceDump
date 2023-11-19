#! /usr/bin/env python3

# Oxylabs - Scraping Dynamic JavaScript Websites - Beautiful Soup Python
# https://youtu.be/Xz514u4V_ts?si=Wbo89TTxSHrJ2fgS

import requests
from bs4 import BeautifulSoup

headers = {
    'X-Requested-With': 'XMLHttpRequest'
}

url = 'https://librivox.org/advanced_search?title=&author=&reader=&keywords=&genre_id=0&status=all&project_type=either&recorded_language=&sort_order=alpha&search_page=1&search_form=advanced&q=the%20time%20machine'

response = requests.get(url, headers=headers)

data = response.json()

soup = BeautifulSoup(data['results'], 'lxml')

book_titles = soup.select('h3 > a')

for title in book_titles:
    print(title.text)
