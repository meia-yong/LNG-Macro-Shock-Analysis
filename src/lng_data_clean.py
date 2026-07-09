import pandas as pd
import numpy as np

print("📂 Loading raw data snapshot...")
# Load the CSV we generated in Phase 1
df = pd.read_csv("raw_lng_macro_data.csv", parse_dates=["Date"], index_col="Date")

# 1. Handle Asynchronous Markets via Forward Fill
# This fills an empty spot with the most recent previous closing price
df_aligned = df.ffill()

# 2. Drop any remaining rows (like the very first day if it started as a NaN)
df_aligned = df_aligned.dropna()

print("\n🔧 Time-Series Alignment Complete.")
print(f"Missing values remaining:\n{df_aligned.isnull().sum()}")

# 3. Calculate Daily Log Returns
# Math: ln(Price_Today / Price_Yesterday)
log_returns = np.log(df_aligned / df_aligned.shift(1))

# Drop the first row of returns because yesterday doesn't exist for day 1
log_returns = log_returns.dropna()

print("\n📈 Log Returns Calculated! Previewing data structure:")
print(log_returns.head())

# Save our clean modeling environment
log_returns.to_csv("clean_lng_log_returns.csv")
print("\n💾 Clean modeling environment exported to 'clean_lng_log_returns.csv'")