# LNG Macro Shock Analysis

An exploratory event-study style analysis of how LNG-linked assets and AUD/USD behave around selected Reserve Bank of Australia (RBA) cash rate announcements.

## Project Overview

This repository studies whether LNG-linked market instruments show different short-horizon behaviour around major RBA cash rate decisions, with particular attention to the distinction between **surprise** and **expected** policy events.

The project uses 10 years of daily market data for:

* **Cheniere Energy (NYSE: LNG)** — a US LNG exporter
* **Woodside Energy (ASX: WDS.AX)** — a major Australian LNG producer
* **AUD/USD** — the Australian dollar exchange rate against the US dollar

Using those series, the repository builds a simple event-study workflow in Python:

1. **download daily price data**
2. **clean and transform the data into daily log returns**
3. **extract return windows around selected RBA event dates**
4. **compare average absolute return behaviour around those events**
5. **visualise the results across assets and event categories**

The analysis is designed as a **portfolio project in financial data handling and event-study construction** rather than a formal empirical paper. Its purpose is to demonstrate a workflow for combining macro event dates with market time series, producing interpretable return-based summaries, and comparing how different assets respond around policy announcements.

---

## Research Question

The project asks two related questions:

### 1) Cross-asset event response

How do LNG-linked assets and AUD/USD behave around selected RBA cash rate announcements?

### 2) Surprise vs expected policy decisions

Do **surprise RBA decisions** appear to generate a larger short-horizon market response than **expected decisions**, as measured by average **absolute daily log returns** in a window around the event date?

The central idea is not to estimate a structural macro model, but to test whether a simple event-window comparison can reveal visibly different volatility patterns around policy shocks.

---

## What this repository actually measures

This project focuses on **absolute daily log returns** around event dates.

That means the main quantity of interest is not raw price change or cumulative abnormal return, but the magnitude of daily movement around an announcement. In practice, the repository asks:

> “When we look at a small window around selected RBA decisions, do these assets move more sharply around some events than others?”

Absolute return is used here as a simple proxy for **market reaction intensity / local volatility**, rather than as a directional measure of whether the asset went up or down.

---

## Assets Used

The repository currently tracks three instruments:

* **`LNG`** — Cheniere Energy
* **`WDS.AX`** — Woodside Energy
* **`AUDUSD=X`** — AUD/USD exchange rate

These assets were chosen to give the project exposure to:

* an **Australian LNG-linked equity**
* a **US LNG-linked equity**
* a **macro FX series directly tied to Australian monetary policy**

This creates a small cross-asset comparison set spanning equities and FX, with one Australian LNG-linked name and one US LNG-linked name.

---

## Data Source and Sample

## Market data source

All price data is pulled from **Yahoo Finance** using the Python package `yfinance`.

## Sample length

The data fetch script downloads **10 years of historical daily data** for each instrument.

## Price field used

The repository uses the **adjusted close price series** from Yahoo Finance and renames it to a clean asset label in the combined dataset.

---

## Repository Workflow

The repository is organised as a linear pipeline across the `src/` directory. Each script performs one stage of the analysis and writes an output file used by the next stage.

## `src/` structure

```text
src/
├─ lng_data_fetch.py
├─ lng_data_clean.py
├─ lng_event_analysis.py
├─ lng_plot_results.py
└─ lng_surprise_engine.py
```

Below is a script-by-script explanation of what each file does.

---

# 1) `lng_data_fetch.py`

## Purpose

Downloads 10 years of daily adjusted close data from Yahoo Finance for the three selected assets and stores them in a single raw CSV.

## Tickers downloaded

The script fetches:

* `LNG`
* `WDS.AX`
* `AUDUSD=X`

## Processing performed

For each ticker, the script:

1. requests historical price data using `yfinance`
2. extracts the **`Adj Close`** column
3. renames that series to a cleaner asset label
4. concatenates the three series into one DataFrame indexed by date

## Output

The result is written to:

```text
raw_lng_macro_data.csv
```

This file is the raw price-level input used by the cleaning step.

---

# 2) `lng_data_clean.py`

## Purpose

Takes the raw price data, handles missing observations, and converts prices into daily log returns.

## Processing performed

This script:

1. reads `raw_lng_macro_data.csv`
2. applies **forward fill** to missing values
3. drops any remaining missing rows
4. computes **daily log returns** for each asset

The return transformation is:

[
r_t = \log\left(\frac{P_t}{P_{t-1}}\right)
]

where (P_t) is the adjusted close price on day (t).

## Why log returns?

Log returns are commonly used in financial time-series analysis because they:

* put different assets on a more comparable scale than price levels
* reduce the non-stationarity issues associated with raw prices
* are additive across time in a way that is often convenient for analysis

## Output

The cleaned return dataset is written to:

```text
clean_lng_log_returns.csv
```

This file is the main input for the event-study scripts.

---

# 3) `lng_event_analysis.py`

## Purpose

Builds a simple event-study style summary around a selected set of RBA event dates.

## Event list used

This script contains a manually specified list of **8 RBA event dates**. These dates are treated as macro shock / policy event dates for the purpose of the analysis.

The dates are hard-coded directly in the script rather than being read from an external event file.

## Event window

For each event, the script extracts a **T−5 to T+5 trading-day window** around the event date, where:

* **T = 0** is the event day
* **T = −5** is five trading days before the event
* **T = +5** is five trading days after the event

So each event contributes an 11-day return window.

## Metric computed

For each asset, the script takes the **absolute value of daily log returns** in each event window. It then averages those absolute-return paths across the 8 selected events.

This produces a mean event-time trajectory of absolute returns for each asset.

In other words, the script is not asking whether the asset rose or fell on average. It is asking whether the asset tended to move **more strongly** around the event.

## Output

The resulting event-time average series is saved to:

```text
macro_shock_trajectory.csv
```

This file contains the mean absolute-return path across the event window for each asset.

---

# 4) `lng_plot_results.py`

## Purpose

Reads the event-study output from `lng_event_analysis.py` and visualises the cross-asset response around the selected RBA event dates.

## Input

This script reads:

```text
macro_shock_trajectory.csv
```

## Plot produced

It generates a chart showing the average absolute return path from **T−5 to T+5** for:

* Cheniere Energy
* Woodside Energy
* AUD/USD

This plot is intended to make it easy to compare whether one asset appears more reactive than another around the selected RBA dates.

---

# 5) `lng_surprise_engine.py`

## Purpose

Runs the repository’s **surprise vs expected** comparison by splitting selected RBA events into two manually defined groups and comparing the average absolute-return trajectory for each group.

This is the part of the repository that produces the project’s “shock vs expected” result.

## Event classification approach

The script contains **two hard-coded event lists**:

* a **shock / surprise** group
* an **expected** group

These are specified manually inside the script.

That means the repository currently treats “surprise” classification as an explicit project assumption rather than as a market-implied estimate derived from interest-rate futures or survey data.

## Event window

As in the earlier event-analysis script, the surprise engine uses a **T−5 to T+5 trading-day window** around each event date.

## Metric computed

For each asset and each event category, the script:

1. extracts the relevant event windows from `clean_lng_log_returns.csv`
2. converts returns to **absolute returns**
3. averages those absolute-return paths across all events in the category

This produces two average trajectories per asset:

* one for **surprise / shock** events
* one for **expected** events

## Plot produced

The script then generates a **shock-vs-expected comparison chart**, which is the main visual result highlighted in the repository.

This chart is designed to show whether the average return magnitude around surprise RBA events is noticeably larger than around expected events.

---

## End-to-End Data Flow

The pipeline can be summarised as:

```text
Yahoo Finance daily adjusted prices
        ↓
raw_lng_macro_data.csv
        ↓
forward fill + drop missing + log returns
        ↓
clean_lng_log_returns.csv
        ↓
selected RBA event windows (T−5 to T+5)
        ↓
absolute return trajectories
        ↓
average event-time profiles and plots
```

Or, script by script:

```text
lng_data_fetch.py
        ↓
lng_data_clean.py
        ↓
lng_event_analysis.py / lng_surprise_engine.py
        ↓
lng_plot_results.py
```

---

## How to Run the Project

## 1) Clone the repository

```bash
git clone https://github.com/meia-yong/LNG-Macro-Shock-Analysis.git
cd LNG-Macro-Shock-Analysis
```

## 2) Install dependencies

If a `requirements.txt` file is not yet included, install the packages used in the scripts manually:

```bash
pip install pandas numpy matplotlib yfinance
```

## 3) Run the pipeline in order

### Step A — fetch raw market data

```bash
python src/lng_data_fetch.py
```

This creates:

```text
raw_lng_macro_data.csv
```

### Step B — clean the price data and compute log returns

```bash
python src/lng_data_clean.py
```

This creates:

```text
clean_lng_log_returns.csv
```

### Step C — build the baseline event-study output

```bash
python src/lng_event_analysis.py
```

This creates:

```text
macro_shock_trajectory.csv
```

### Step D — plot the baseline cross-asset event response

```bash
python src/lng_plot_results.py
```

This generates the cross-asset event-study chart based on the average absolute-return trajectory around the selected RBA dates.

### Step E — run the surprise vs expected comparison

```bash
python src/lng_surprise_engine.py
```

This generates the **shock vs expected** comparison output and chart.

---

## Files Produced by the Current Pipeline

Depending on which scripts are run, the repository generates several intermediate and final outputs.

## Core CSV outputs

* `raw_lng_macro_data.csv` — raw adjusted close price data downloaded from Yahoo Finance
* `clean_lng_log_returns.csv` — cleaned daily log returns
* `macro_shock_trajectory.csv` — mean absolute-return event path for the selected 8-event sample

## Plot outputs

The repository also generates chart output for:

* the **cross-asset average event response**
* the **shock vs expected comparison**

The exact image filenames depend on the current plotting code and output settings.

---

## Methodological Summary

At a high level, the repository performs the following analysis:

## Step 1: Collect daily market data

Download 10 years of adjusted close prices for LNG, WDS.AX, and AUD/USD.

## Step 2: Convert prices into returns

Use daily log returns to put the series on a common scale suitable for event analysis.

## Step 3: Select event dates

Use manually specified RBA cash-rate announcement dates as event anchors.

## Step 4: Build event windows

For each event, extract an 11-trading-day window from **T−5 to T+5**.

## Step 5: Measure return magnitude

Take the **absolute value** of returns within each event window.

## Step 6: Average across events

Average those absolute-return windows across all events in a category.

## Step 7: Compare patterns visually

Plot the average event-time paths and compare how assets behave around:

* the selected macro event sample
* surprise vs expected RBA events

---

## What the Main Result Means

The repository’s key result is the **shock vs expected** comparison.

The interpretation of that chart is:

* if the **shock** line sits above the **expected** line near **T = 0**, then surprise RBA events were associated with **larger average absolute daily moves** than expected decisions over that event window
* if the difference is especially visible for **Woodside**, that suggests the Australian LNG-linked equity may have shown a stronger local response to those surprise events than to routine decisions
* if the same pattern is weaker for **Cheniere** or **AUD/USD**, that suggests the response may not be uniform across all instruments in the sample

This is an event-study style comparison of **average return magnitude**, not a directional prediction or a formal causal estimate.

---

## Interpretation: what can be claimed safely

A careful reading of the current implementation would support claims like the following:

* The project finds that **average absolute return behaviour differs across selected RBA event categories** in this sample.
* Some assets appear to show a **larger immediate movement around hand-labelled surprise decisions** than around expected decisions.
* The methodology provides a compact way to compare event-window behaviour across multiple assets using a common return metric.

These are reasonable claims for the current codebase.

---

## Interpretation: what the current repository does *not* establish

The present implementation should **not** be described as proving any of the following:

* that RBA surprises causally drive the full observed return pattern
* that the project formally tests or rejects the **Efficient Market Hypothesis**
* that the identified events are objectively measured “surprises” in a market-implied sense
* that the results represent abnormal returns relative to a benchmark model
* that the observed differences are statistically significant without additional testing

Those would require a more formal empirical setup than the current repository implements.

---

## Strengths of the Current Project

Even in its current form, the repository demonstrates several useful skills:

### 1) Multi-asset financial data handling

The project works with:

* Australian equity data
* US equity data
* FX data

and brings them into a common event-study framework.

### 2) Clean pipeline structure

The project is broken into separate scripts for:

* data collection
* cleaning / return construction
* event analysis
* plotting
* surprise-vs-expected comparison

That makes the workflow easy to follow and easy to extend.

### 3) Applied macro-financial framing

Rather than using a generic toy dataset, the project is built around a real market question:
how energy-linked assets behave around monetary-policy events.

### 4) Sensible return transformation

Using log returns and event windows is an appropriate starting point for a small-scale exploratory financial analysis project.

### 5) Clear visual output

The shock-vs-expected chart gives a compact summary of the core comparison and makes the result accessible without requiring a large amount of econometric machinery.

---

## Limitations and Caveats

This section matters because it defines what the repository is and is not trying to do.

## 1) Surprise classification is manually specified

The shock and expected event lists are hard-coded in `lng_surprise_engine.py`.

That means the project currently does **not** derive surprise magnitude from:

* OIS pricing
* interest-rate futures
* survey expectations
* market-implied policy paths

So “surprise” should be interpreted as a **manual project classification**, not a formal monetary-policy surprise measure.

## 2) Daily data limits timing precision

The analysis uses **daily adjusted close prices**, not intraday data.

That means it cannot isolate minute-by-minute market reactions to the RBA announcement itself, and it also makes cross-market timing more approximate when comparing:

* Australian equities
* US equities
* FX

## 3) Time-zone alignment is simplified

Because the project works at daily frequency, event alignment is necessarily approximate. The repository does not currently implement a full exchange-calendar and timestamp-based alignment framework across ASX, NYSE, and FX markets.

## 4) Absolute returns are a simple proxy

The project uses **absolute daily log returns** as a measure of reaction intensity. This is useful for exploratory work, but it is not the same as a full volatility model, abnormal-return framework, or event-induced variance test.

## 5) No formal significance testing

The current implementation is descriptive and visual. It does not currently report:

* t-tests
* bootstrap intervals
* non-parametric tests
* regression-based event-study estimates
* benchmark-adjusted abnormal returns

So differences in plotted lines should be treated as exploratory patterns rather than statistically validated conclusions.

## 6) Small event sample

The project relies on a small set of selected RBA dates. With small event counts, average event paths can be sensitive to the inclusion or exclusion of individual observations.

## 7) Other macro and commodity forces may matter

LNG-linked assets are affected by many factors besides Australian monetary policy, including:

* global gas and energy prices
* commodity-market news
* equity-market sentiment
* firm-specific developments
* US macro conditions

So any event-window pattern around RBA dates should be interpreted cautiously.

---

## How I would extend this project next

There are several natural next steps if this repository were developed further.

## 1) Move event dates into an external event file

Instead of hard-coding dates in the scripts, create something like:

```text
data/rba_events.csv
```

with columns such as:

```text
date,event_type,notes
2022-05-03,shock,RBA surprise rate increase
...
```

That would make the event logic more transparent and easier to audit.

## 2) Add formal statistical testing

Examples:

* compare surprise vs expected event-window absolute returns using **Mann–Whitney U**
* test mean differences with bootstrap confidence intervals
* compare day-0 and cumulative-window responses separately

## 3) Add a results table to the repository

A useful summary table might include:

* number of events in each category
* mean day-0 absolute return
* median day-0 absolute return
* average cumulative absolute return over the event window
* simple test statistics for surprise vs expected differences

## 4) Use intraday or higher-frequency data

If intraday data were available, the project could align RBA announcement timestamps much more precisely and produce a cleaner event-study design.

## 5) Expand the asset universe

The analysis could be extended to:

* Santos or other Australian energy names
* Australian market index ETFs
* bond yields or rate-sensitive equity sectors
* additional FX pairs

## 6) Replace manual surprise labels with market-implied surprise measures

A stronger version of the project would classify surprises using:

* OIS pricing
* futures-implied expectations
* market consensus estimates from professional sources

## 7) Add benchmark-adjusted event-study metrics

Instead of only absolute returns, future versions could include:

* abnormal returns relative to a market model
* realised volatility measures
* cumulative abnormal returns
* regression-based event-study estimates

---

## Suggested Interpretation of the Repository

The best way to read this project is as:

> a compact exploratory macro-financial event-study pipeline that uses daily Yahoo Finance data to compare how LNG-linked assets and AUD/USD move around selected RBA cash-rate decisions, including a manual surprise-vs-expected split.

That framing matches the implementation closely and captures the project’s real strengths:

* a clear applied question
* sensible data handling
* a reproducible Python workflow
* cross-asset event analysis
* and a visible attempt to move beyond purely descriptive price charts into event-based financial analysis

---

## Tech Stack

* **Python**
* **pandas**
* **numpy**
* **matplotlib**
* **yfinance**

---

## Future Improvements to the Repository Itself

To make the repository stronger as a public portfolio project, I would add:

* a `requirements.txt`
* an `events.csv` file containing all event labels
* saved plot filenames documented in the README
* a `data/` folder structure separating raw and processed outputs
* a short results table in the README
* comments in the scripts describing assumptions and output files
* a note on exactly how shock vs expected events were selected

---

## Closing Note

This project is intended as an exploratory applied-finance portfolio piece rather than a final research paper. Its value lies in showing the ability to:

* formulate a market question
* fetch and clean multi-asset financial data
* construct log-return event windows
* compare market behaviour around macro events
* and communicate the result in a reproducible Python workflow
