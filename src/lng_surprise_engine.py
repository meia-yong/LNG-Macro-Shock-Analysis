import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("📂 Ingesting clean returns...")
returns_df = pd.read_csv("clean_lng_log_returns.csv", parse_dates=["Date"], index_col="Date")

# 1. Categorize our 10-year events into Expected vs Surprise Shocks
# We isolate the unexpected or aggressive double-moves from the standard ones
shocks = pd.to_datetime([
    "2016-05-03",  # Surprise cut breaking a long holding cycle
    "2020-03-19",  # Historic emergency pandemic cut
    "2022-05-03",  # First post-pandemic inflation hike (shock regime shift)
    "2022-06-07",  # Massive outsized +50 bps double-hike
    "2023-11-07"   # The aggressive Melbourne Cup day inflation-busting hike
])

expected = pd.to_datetime([
    "2016-08-02", "2019-06-04", "2019-07-02", "2019-10-01", "2020-03-03",
    "2020-11-03", "2022-07-05", "2022-08-02", "2022-09-06", "2022-10-04",
    "2022-11-01", "2022-12-06", "2023-02-07", "2023-03-07", "2023-05-02",
    "2023-06-06", "2025-02-18", "2025-05-20", "2025-08-12", "2026-02-03",
    "2026-03-17", "2026-05-05"
])

def extract_trajectory(event_list, window_size=5):
    all_windows = []
    for date in event_list:
        if date in returns_df.index:
            pos = returns_df.index.get_loc(date)
            chunk = returns_df.iloc[pos-window_size : pos+window_size+1].copy()
            chunk['Relative_Day'] = np.arange(-window_size, window_size + 1)
            all_windows.append(chunk.set_index('Relative_Day'))
    # Return mean absolute volatility scaled to a percentage (%)
    return pd.concat(all_windows).abs().groupby(level=0).mean() * 100

# Compute trajectories for both groups
shock_trajectory = extract_trajectory(shocks)
expected_trajectory = extract_trajectory(expected)

# 2. Plotting the Comparison for our Resume Visuals
plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Panel 1: The Surprise Shock Trajectory
ax1.plot(shock_trajectory.index, shock_trajectory['AUS_LNG_Leader'], marker='s', color='#ff7f0e', linewidth=2.5, label='Woodside LNG (ASX)')
ax1.plot(shock_trajectory.index, shock_trajectory['Aussie_Dollar'], marker='o', color='#1f77b4', linewidth=2.5, label='Aussie Dollar (FX)')
ax1.axvline(x=0, color='red', linestyle='--', alpha=0.7)
ax1.set_title('🚨 Macro Surprise Shocks (Unexpected Pivot Days)', fontweight='bold')
ax1.set_xlabel('Relative Days Timeline')
ax1.set_ylabel('Mean Absolute Return (%)')
ax1.legend()

# Panel 2: The Expected Consensus Trajectory
ax2.plot(expected_trajectory.index, expected_trajectory['AUS_LNG_Leader'], marker='s', color='#ff7f0e', alpha=0.5, label='Woodside LNG (ASX)')
ax2.plot(expected_trajectory.index, expected_trajectory['Aussie_Dollar'], marker='o', color='#1f77b4', alpha=0.5, label='Aussie Dollar (FX)')
ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.7)
ax2.set_title('💤 Consensus Events (Priced-In Decisions)', fontweight='bold')
ax2.set_xlabel('Relative Days Timeline')

plt.suptitle('Decomposing the Efficient Market Hypothesis: Shocks vs. Priced-In Macro Signals', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig("shock_vs_expected_chart.png", dpi=300)
print("🎨 Dual-panel analysis visualization generated and exported as 'shock_vs_expected_chart.png'!")
plt.show()