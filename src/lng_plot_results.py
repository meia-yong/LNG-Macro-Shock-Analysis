import pandas as pd
import matplotlib.pyplot as plt

print("Ingesting macro shock matrix...")
# Load the matrix we generated in Phase 3
trajectory_df = pd.read_csv("macro_shock_trajectory.csv", index_col="Relative_Day")

# Convert values to percentages for professional scanning
trajectory_pct = trajectory_df * 100

# Set up a high-quality data science plot style
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each asset class with institutional coloring
ax.plot(trajectory_pct.index, trajectory_pct['Aussie_Dollar'], marker='o', linewidth=2.5, color='#1f77b4', label='Aussie Dollar (FX)')
ax.plot(trajectory_pct.index, trajectory_pct['AUS_LNG_Leader'], marker='s', linewidth=2.5, color='#ff7f0e', label='Woodside Energy (ASX:WDS)')
ax.plot(trajectory_pct.index, trajectory_pct['US_LNG_Leader'], marker='^', linewidth=2.5, color='#2ca02c', label='Cheniere Energy (NYSE:LNG)')

# Highlight the central bank announcement day (T=0)
ax.axvline(x=0, color='red', linestyle='--', linewidth=1.5, label='RBA Announcement Day (T=0)')

# Formatting details to look production-ready
ax.set_title('10-Year Cross-Asset Volatility Trajectory Surrounding RBA Decisions', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Relative Days Timeline (T-5 to T+5)', fontsize=12, labelpad=10)
ax.set_ylabel('Mean Absolute Daily Return (%)', fontsize=12, labelpad=10)
ax.set_xticks(trajectory_pct.index)

ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='none')
plt.tight_layout()

# Save the plot directly as a PNG to push to GitHub
plt.savefig("rba_macro_volatility_chart.png", dpi=300)
print("🎨 Professional chart generated and saved as 'rba_macro_volatility_chart.png'!")
plt.show()