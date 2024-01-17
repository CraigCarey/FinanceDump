#! /usr/bin/env python3

import yfinance as yf

def get_valuation_ratios(ticker):
    stock = yf.Ticker(ticker)
    
    # Get key financial data
    key_stats = stock.info

    # Extract relevant information
    market_cap = key_stats.get('marketCap', None)
    pe_ratio = key_stats.get('trailingPE', None)
    pb_ratio = key_stats.get('priceToBook', None)
    dividend_yield = key_stats.get('dividendYield', None)
    ev_to_ebitda = key_stats.get('enterpriseToEbitda', None)

    # Print the calculated ratios
    print(f"Market Cap: {market_cap}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"P/B Ratio: {pb_ratio}")
    print(f"Dividend Yield: {dividend_yield}")
    print(f"EV/EBITDA: {ev_to_ebitda}")

# Example usage
ticker_symbol = "AAPL"  # Replace with the desired stock ticker
get_valuation_ratios(ticker_symbol)
