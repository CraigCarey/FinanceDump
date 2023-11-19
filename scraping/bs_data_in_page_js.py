#! /usr/bin/env python3

# Oxylabs - Scraping Dynamic JavaScript Websites - Beautiful Soup Python
# https://youtu.be/Xz514u4V_ts?si=Wbo89TTxSHrJ2fgS

import requests
from bs4 import BeautifulSoup
import re
import json

response = requests.get('https://quotes.toscrape.com/js')

soup = BeautifulSoup(response.text, 'lxml')

script_tag = soup.find('script', src=None)

pattern = 'var data =(.+?);\n'

raw_data = re.findall(pattern, script_tag.string, re.S)

# print(raw_data)

if raw_data:
    data = json.loads(raw_data[0])
else:
    raise RuntimeError('Data not found')

print(data)
