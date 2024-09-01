# NavNinja

## Gathering basic NAV data from HL

```bash

cd ../scraping/

# Gets a list of trusts and pickles it
./get_hl_trusts.py

# Takes the pickled list from above and obtains the nav etc for each entry
../scraping/get_hl_trust_navs.py
```
