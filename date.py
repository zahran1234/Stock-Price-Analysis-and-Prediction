import yfinance as yf

# Specify the stock symbol (ticker)
ticker_symbol = "AAPL"

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

# Get historical earnings data
earnings_history = ticker.get_earnings_dates

# Print the historical earnings data
print(earnings_history)
