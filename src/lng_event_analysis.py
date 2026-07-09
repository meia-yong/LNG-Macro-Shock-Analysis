import pandas as pd
import numpy as np

print("Ingesting clean log returns...")
# Load the clean log returns dataset we engineered in Phase 2
returns_df = pd.read_csv("clean_lng_log_returns.csv", parse_dates=["Date"], index_col="Date")

# 1. Define our Macro Shock Event Dates (RBA Interest Rate Announcements)
# Key historical pivot points in monetary policy
rba_event_dates = [
    "2016-05-03",  # Rate cut to 1.75% (Surprise easing cycle start)
    "2016-08-02",  # Rate cut to 1.50%
    "2019-06-04",  # Rate cut to 1.25% (Pre-pandemic easing)
    "2020-03-19",  # Emergency pandemic cut to 0.25% (Major global shock)
    "2022-05-03",  # First post-pandemic inflation HIKE (+25 bps)
    "2022-06-07",  # Outsized surprise hike (+50 bps)
    "2022-10-04",  # Pivot to smaller +25 bps hikes
    "2023-11-07",  # Melbourne Cup day hike to 4.35%
]

# Convert text dates into pandas datetime timestamps
event_timestamps = pd.to_datetime(rba_event_dates)
print("Successfully loaded {len(event_timestamps)} macro regime event windows.")

# 2. Slice temporal windows around each event date (T-5 to T+5)
window_size = 5
all_event_windows = []

for event_date in event_timestamps:
    if event_date in returns_df.index:
        # Get the integer row position of the event date
        idx_pos = returns_df.index.get_loc(event_date)
        
        # Calculate start and end indices for our 11-day window
        start_pos = idx_pos - window_size
        end_pos = idx_pos + window_size + 1
        
        # Slice out the row chunk
        event_chunk = returns_df.iloc[start_pos:end_pos].copy()
        
        # Re-index from absolute dates to relative days: -5, -4, ..., 0, ..., 4, 5
        event_chunk['Relative_Day'] = np.arange(-window_size, window_size + 1)
        event_chunk = event_chunk.set_index('Relative_Day')
        
        all_event_windows.append(event_chunk)

# 3. Collapse all windows to find the mean baseline directional movement
mean_event_trajectory = pd.concat(all_event_windows).groupby(level=0).mean()

# 4. Collapse all windows using ABSOLUTE returns to measure true Volatility Shocks
# Math: |Return| gives us the size of the swing, regardless of up or down
mean_volatility_trajectory = pd.concat(all_event_windows).abs().groupby(level=0).mean()

print("Cross-Asset Volatility Shock Trajectory (Mean Absolute Movement):")
print(mean_volatility_trajectory)

# Save our output matrix for visualization later
mean_volatility_trajectory.to_csv("macro_shock_trajectory.csv")
print("Macro shock matrix saved to 'macro_shock_trajectory.csv'")