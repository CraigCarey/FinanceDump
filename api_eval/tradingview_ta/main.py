#! /usr/bin/env python3

import tradingview_ta as ta

# Define the ticker symbol and exchange
symbol = "GAZP"
exchange = "MOEX"  # Moscow Exchange

# Create a TradingView object for the given symbol and exchange
ticker = ta.TA_Handler(
    symbol=symbol,
    screener="russia",  # Country screener, use 'russia' for MOEX
    exchange=exchange,
    interval=ta.Interval.INTERVAL_1_DAY  # Interval for the data
)

# Get the analysis data
analysis = ticker.get_analysis()

# Extract the current price
current_price = analysis.indicators["close"]

print(f"The current price of {symbol} is {current_price} RUB")

# Define a list of tickers and their respective exchanges
tickers = [
    {"symbol": "GAZP", "exchange": "MOEX"},  # Gazprom
    {"symbol": "AAPL", "exchange": "NASDAQ"},  # Apple
    {"symbol": "TSLA", "exchange": "NASDAQ"},  # Tesla
    {"symbol": "SBER", "exchange": "MOEX"},  # Sberbank
    # Add more tickers as needed
]

# Define the screener based on the exchange
screeners = {
    "MOEX": "russia",
    "NASDAQ": "america",
    # Add other exchanges and their screeners as needed
}

# Function to get the current price for a given ticker
def get_current_price(symbol, exchange):
    try:
        ticker = ta.TA_Handler(
            symbol=symbol,
            screener=screeners[exchange],
            exchange=exchange,
            interval=ta.Interval.INTERVAL_1_DAY  # Interval for the data
        )
        analysis = ticker.get_analysis()
        current_price = analysis.indicators["close"]
        return current_price
    except Exception as e:
        return f"Error fetching data for {symbol}: {e}"

# Loop through each ticker and get the current price
for ticker_info in tickers:
    symbol = ticker_info["symbol"]
    exchange = ticker_info["exchange"]
    price = get_current_price(symbol, exchange)
    print(f"The current price of {symbol} on {exchange} is {price}")
