# Design

### Scraping holdings

- Get raw list of holdings
- hash it
- compare with db trust table
- has it changed since last update? If so...
- for each holding:
- is it in the securities table? Search by SEDOL, FIGI & ISIN
- if not...
- find the SEDOL FIGI and ISIN
    - if SEDOL and ISIN are a match they'll have the same FIGI
- add to securities table


### Calculating NAV, aggregate metrics
Fetching data should perhaps be a separate service

- for each holding
- check security_data table, is the updatedAt > someDuration? If so...
- fetch data & update updatedAt
- calculate metrics
- aggregate metrics & calculate true NAV

### Components
- DB & ORM
- trust scraper
- security scraper
- metrics calculator
