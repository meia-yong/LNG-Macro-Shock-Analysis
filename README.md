# LNG Macro Shock Engine: A 10-Year Cross-Asset Event Study
An empirical investigation into time-series volatility anomalies and market efficiency across global Liquefied Natural Gas (LNG) equities and commodity currencies surrounding central bank intervention.

## Core Research Objective
Can we isolate structural market anomalies during monetary policy updates? This project constructs an asynchronous event-study pipeline using a 10-year historical window (2016–2026) to test the **Efficient Market Hypothesis (EMH)** against the Reserve Bank of Australia (RBA) cash rate decisions.

### Key Dimensions Modeled:
* **Asset Ecosystem:** Woodside Energy (ASX: WDS), Cheniere Energy (NYSE: LNG), and the AUD/USD currency pairing.
* **The Regime Split:** Segregating priced-in consensus announcements from surprise policy shocks.

## Analytical Insights & Methodology
1. **Asynchronous Market Alignment:** Resolved multi-time-zone structural gaps between NYSE, ASX, and FX global closing schedules using forward-fill synchronization without look-ahead bias.
2. **Log-Return Stationary Conversion:** Transformed price series into stationary logarithmic metrics to isolate pure variance changes.
3. **The Surprise Multiplication Effect:** While standard interest rate decisions resulted in a completely flat volatility baseline, official surprise shocks triggered an instantaneous **2x volatility multiplication spike** in domestic energy producers on Day 0 ($T=0$).

### Performance Visualizations
| Consensus vs. Monetary Shocks Decomposed |
| :---: |
| ![Shock vs Expected](./shock_vs_expected_chart.png) |

## Tech Stack & Implementation
* **Language:** Python
* **Libraries:** `pandas` (time-series alignment), `numpy` (log returns), `yfinance` (market data aggregation), `matplotlib` (data visualization)
* **Architecture:** Modular script execution pipeline (`fetch` ➡️ `clean` ➡️ `model` ➡️ `decompose`).
