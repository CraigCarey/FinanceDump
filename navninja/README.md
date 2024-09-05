# NavNinja

## Gathering basic NAV data from HL

```bash

cd ../scraping/

# Gets a list of trusts and writes to csv 
# Writes to ../data/investment_trusts_240905.csv
./get_hl_trusts.py

# Takes the list from above and obtains the nav etc for each entry
# Writes to ../data/investment_trust_data_240905.csv
../scraping/get_hl_trust_data.py
```
