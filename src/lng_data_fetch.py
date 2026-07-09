import yfinance as yf
import pandas as pd

# 1. Define the tickers we want to explore
tickers = {
    "US_LNG_Leader": "LNG",         # Cheniere Energy
    "AUS_LNG_Leader": "WDS.AX",     # Woodside Energy
    "Aussie_Dollar": "AUDUSD=X"     # FX Rate
}

print("🔄 Initializing live data pipeline from Yahoo Finance...")

# 2. Fetch 10 years of daily historical data
# We add auto_adjust=True so Yahoo automatically handles stock splits/dividends in the 'Close' column
raw_data = yf.download(
    list(tickers.values()), 
    start="2016-01-01", 
    end="2026-01-01", 
    auto_adjust=True
)

# 3. Safely extract the closing prices
# When downloading multiple tickers, 'Close' becomes the top-level column index
adj_close_prices = raw_data['Close']

# 4. Rename columns so they are clean and easy to inspect
adj_close_prices = adj_close_prices.rename(columns={v: k for k, v in tickers.items()})

# 5. Let's inspect the structural shape of our dataframe
print("\n📊 Pipeline Complete! Initial Dataset Structure:")
print(adj_close_prices.head())

print("\n🔍 Missing value summary:")
print(adj_close_prices.isnull().sum())

# Save it to a CSV file in your working directory to freeze the raw snapshot
adj_close_prices.to_csv("raw_lng_macro_data.csv")
print("\n💾 Raw market data frozen and exported to 'raw_lng_macro_data.csv'")