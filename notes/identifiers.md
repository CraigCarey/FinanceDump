# Identifiers

### ISIN (International Securities Identification Number)

- Global standard for identifying securities, governed by ISO 6166.
- Available for virtually all publicly traded securities worldwide, making it widely used in global contexts.
- Often requires access to financial data providers (like Bloomberg or Refinitiv) to retrieve detailed ISINs for specific securities.
- 12 characters long.
- Structure:
    - First 2 characters: Country code (based on ISO 3166-1 alpha-2).
    - Next 9 characters: Security identifier (national or local identifier, often derived from systems like CUSIP or SEDOL).
    - Last character: Check digit for validation.
    - Example: US0378331005 (Apple Inc.)

### CIK (Central Index Key)

- Primarily used in the United States by the SEC (Securities and Exchange Commission).
- Easily accessible because it's used for filings in the SEC's EDGAR database.
- Most commonly available for U.S.-based public companies, mutual funds, and related entities.

### CUSIP (Committee on Uniform Securities Identification Procedures)

- Primarily used in the U.S. and Canada for identifying North American securities.
- Commonly used for trading and settlement purposes.
- Access to CUSIP data often requires paid subscriptions, as it's proprietary to the CUSIP Global Services (CGS).

### SEDOL

- A unique identifier specific to securities traded in the United Kingdom and Ireland.
- Managed by the London Stock Exchange (LSE).
- Primarily used in domestic contexts, although it may appear in global financial datasets.
