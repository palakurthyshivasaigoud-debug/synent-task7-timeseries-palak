"""
============================================================
  SYNENT TECHNOLOGIES - DATA SCIENCE INTERNSHIP
  Task 7: Time Series Analysis
  Name   : Palak
  Dataset: Stock Price Dataset
============================================================

Task Objectives:
  - Trend analysis
  - Seasonality detection
  - Optional forecast future values
Output:
  - Time-based insights report with graphs
"""

import os
import sys
import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

# Always resolve outputs relative to this script's location
_BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASE)

# ============================================================
#  CONFIGURATION - UPDATE THIS PATH TO YOUR DATASET
# ============================================================

DATA_PATH = os.path.join(_BASE, "CIPLA.csv")

# If your dataset uses different names, update these after sharing the file/path.
DATE_COLUMN = "Date"
PRICE_COLUMN = "Close"

# ============================================================

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10

os.makedirs("data/charts", exist_ok=True)

print("=" * 60)
print("   TASK 7 - TIME SERIES ANALYSIS")
print("   Stock Price Dataset")
print("   Synent Technologies Data Science Internship")
print("=" * 60)


def find_column(df, preferred, alternatives):
    """Find a column by preferred name or common alternatives."""
    normalized = {col.strip().lower().replace(" ", "_"): col for col in df.columns}
    candidates = [preferred] + alternatives
    for candidate in candidates:
        key = candidate.strip().lower().replace(" ", "_")
        if key in normalized:
            return normalized[key]
    return None


def add_takeaway(fig, lines):
    """Add a short insight note under a chart."""
    fig.subplots_adjust(bottom=0.22)
    fig.text(
        0.5,
        0.03,
        "\n".join(lines),
        ha="center",
        va="bottom",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#f7f7f7", edgecolor="#cccccc"),
    )


# ============================================================
#  PHASE 1: DATA CLEANING & PREPROCESSING
# ============================================================
print("\n" + "=" * 60)
print("  PHASE 1: DATA CLEANING & PREPROCESSING")
print("=" * 60)

print(f"\n>> Loading dataset from: {DATA_PATH}")
if not os.path.exists(DATA_PATH):
    print(f"\n   ERROR: File not found -> {DATA_PATH}")
    print("   Please update DATA_PATH at the top of this script.")
    sys.exit(1)

try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(f"   ERROR reading file: {e}")
    sys.exit(1)

print(f"   Raw shape : {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"   Columns   : {list(df.columns)}")

date_col = find_column(df, DATE_COLUMN, ["date", "timestamp", "datetime"])
price_col = find_column(df, PRICE_COLUMN, ["close", "adj close", "adj_close", "price", "last"])

if date_col is None:
    print("\n   ERROR: Date column not found.")
    print("   Update DATE_COLUMN at the top of this script.")
    sys.exit(1)

if price_col is None:
    print("\n   ERROR: Price column not found.")
    print("   Update PRICE_COLUMN at the top of this script.")
    sys.exit(1)

print(f"\n>> Using date column : {date_col}")
print(f">> Using price column: {price_col}")

df = df.rename(columns={date_col: "Date", price_col: "Close"})

print("\n>> Cleaning data...")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Close"] = pd.to_numeric(df["Close"].astype(str).str.replace(",", ""), errors="coerce")

before_rows = len(df)
df = df.dropna(subset=["Date", "Close"])
df = df.drop_duplicates()
df = df.sort_values("Date").reset_index(drop=True)
after_rows = len(df)

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()
df["YearMonth"] = df["Date"].dt.to_period("M")
df["Daily_Return_%"] = df["Close"].pct_change() * 100
df["MA_20"] = df["Close"].rolling(window=20).mean()
df["MA_50"] = df["Close"].rolling(window=50).mean()

print(f"   Rows removed during cleaning: {before_rows - after_rows:,}")
print(f"   Clean shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"   Date range : {df['Date'].min().date()} -> {df['Date'].max().date()}")
print("   [Data Cleaning Complete]")


# ============================================================
#  PHASE 2: SUMMARY STATISTICS
# ============================================================
print("\n" + "=" * 60)
print("  PHASE 2: SUMMARY STATISTICS")
print("=" * 60)

start_price = df["Close"].iloc[0]
end_price = df["Close"].iloc[-1]
highest_price = df["Close"].max()
lowest_price = df["Close"].min()
highest_date = df.loc[df["Close"].idxmax(), "Date"]
lowest_date = df.loc[df["Close"].idxmin(), "Date"]
overall_change = end_price - start_price
overall_change_pct = (overall_change / start_price) * 100
avg_daily_return = df["Daily_Return_%"].mean()
volatility = df["Daily_Return_%"].std()

print(f"""
   Start Price          : ${start_price:,.2f}
   End Price            : ${end_price:,.2f}
   Overall Change       : ${overall_change:,.2f} ({overall_change_pct:.2f}%)
   Highest Close Price  : ${highest_price:,.2f} on {highest_date.date()}
   Lowest Close Price   : ${lowest_price:,.2f} on {lowest_date.date()}
   Avg Daily Return     : {avg_daily_return:.3f}%
   Daily Volatility     : {volatility:.3f}%
""")


# ============================================================
#  PHASE 3: TIME SERIES ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("  PHASE 3: TIME SERIES ANALYSIS")
print("=" * 60)

monthly = df.groupby("YearMonth")["Close"].mean().reset_index()
monthly["YearMonth_str"] = monthly["YearMonth"].astype(str)

yearly = df.groupby("Year")["Close"].mean()
best_year = yearly.idxmax()
worst_year = yearly.idxmin()

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
seasonality = df.groupby("Month_Name")["Close"].mean().reindex(month_order)
best_month = seasonality.idxmax()
worst_month = seasonality.idxmin()

print("\n>> Trend Analysis")
print(f"   Best average year : {best_year} (${yearly.max():,.2f})")
print(f"   Worst average year: {worst_year} (${yearly.min():,.2f})")
print(f"   Overall movement  : {'Upward' if overall_change >= 0 else 'Downward'}")

print("\n>> Seasonality Analysis")
print(f"   Highest average month: {best_month} (${seasonality.max():,.2f})")
print(f"   Lowest average month : {worst_month} (${seasonality.min():,.2f})")

print("\n   [Analysis Complete]")


# ============================================================
#  PHASE 4: VISUALIZATION
# ============================================================
print("\n" + "=" * 60)
print("  PHASE 4: VISUALIZATION")
print("=" * 60)
print("\n   Generating charts...")
print("   Each graph will open on screen. Close the graph window to see the next one.\n")

for file_name in os.listdir("data/charts"):
    if file_name.lower().endswith(".png"):
        os.remove(os.path.join("data/charts", file_name))


# Chart 1: Closing price trend
print(">> Chart 1/4: Closing Price Trend")
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(df["Date"], df["Close"], color="#2f6f9f", linewidth=1.8)
ax.set_title("Stock Closing Price Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: f"${value:,.0f}"))
ax.grid(alpha=0.35)
add_takeaway(fig, [
    f"Highest close: ${highest_price:,.2f} on {highest_date.date()}",
    f"Lowest close: ${lowest_price:,.2f} on {lowest_date.date()}",
])
plt.tight_layout(rect=[0, 0.16, 1, 1])
plt.savefig("data/charts/01_closing_price_trend.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig)
print("   Saved: 01_closing_price_trend.png")


# Chart 2: Moving averages
print("\n>> Chart 2/4: Moving Average Trend")
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(df["Date"], df["Close"], label="Close", color="#7a7a7a", linewidth=1.2, alpha=0.8)
ax.plot(df["Date"], df["MA_20"], label="20-Day MA", color="#2ca25f", linewidth=1.8)
ax.plot(df["Date"], df["MA_50"], label="50-Day MA", color="#de2d26", linewidth=1.8)
ax.set_title("Short-Term vs Long-Term Moving Average")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: f"${value:,.0f}"))
ax.legend()
ax.grid(alpha=0.35)
latest_ma20 = df["MA_20"].dropna().iloc[-1] if not df["MA_20"].dropna().empty else np.nan
latest_ma50 = df["MA_50"].dropna().iloc[-1] if not df["MA_50"].dropna().empty else np.nan
trend_signal = "Bullish / upward" if latest_ma20 >= latest_ma50 else "Bearish / downward"
add_takeaway(fig, [
    f"Latest 20-day average: ${latest_ma20:,.2f}",
    f"Latest 50-day average: ${latest_ma50:,.2f} | Signal: {trend_signal}",
])
plt.tight_layout(rect=[0, 0.16, 1, 1])
plt.savefig("data/charts/02_moving_averages.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig)
print("   Saved: 02_moving_averages.png")


# Chart 3: Monthly average seasonality
print("\n>> Chart 3/4: Monthly Seasonality")
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(seasonality.index, seasonality.values, color=sns.color_palette("Blues", 12), edgecolor="white")
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h, f"${h:,.0f}", ha="center", va="bottom", fontsize=8)
ax.set_title("Average Close Price by Month")
ax.set_xlabel("Month")
ax.set_ylabel("Average Close Price")
ax.tick_params(axis="x", rotation=45)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: f"${value:,.0f}"))
ax.grid(axis="y", alpha=0.35)
add_takeaway(fig, [
    f"Highest average month: {best_month} (${seasonality.max():,.2f})",
    f"Lowest average month: {worst_month} (${seasonality.min():,.2f})",
])
plt.tight_layout(rect=[0, 0.18, 1, 1])
plt.savefig("data/charts/03_monthly_seasonality.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig)
print("   Saved: 03_monthly_seasonality.png")


# Chart 4: Future trend prediction
print("\n>> Chart 4/4: Future Trend Prediction")
forecast_days = 30
recent = df.tail(min(90, len(df))).copy()
recent = recent.reset_index(drop=True)
future_dates = pd.date_range(df["Date"].iloc[-1] + pd.Timedelta(days=1), periods=forecast_days, freq="D")

if len(recent) >= 2:
    x_recent = np.arange(len(recent))
    slope, intercept = np.polyfit(x_recent, recent["Close"], 1)
    fitted_recent = intercept + slope * x_recent
    x_future = np.arange(len(recent), len(recent) + forecast_days)
    future_prices = intercept + slope * x_future
    residual_std = (recent["Close"] - fitted_recent).std()
else:
    slope = 0
    future_prices = np.repeat(end_price, forecast_days)
    residual_std = 0

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Forecast_Close": future_prices,
})
forecast_df["Lower_Band"] = forecast_df["Forecast_Close"] - residual_std
forecast_df["Upper_Band"] = forecast_df["Forecast_Close"] + residual_std

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(recent["Date"], recent["Close"], label="Recent Actual Close", color="#2f6f9f", linewidth=1.8)
ax.plot(forecast_df["Date"], forecast_df["Forecast_Close"], label="Predicted Future Trend", color="#f28e2b", linestyle="--", linewidth=2)
ax.fill_between(
    forecast_df["Date"],
    forecast_df["Lower_Band"],
    forecast_df["Upper_Band"],
    color="#f28e2b",
    alpha=0.18,
    label="Prediction Range",
)
ax.axvline(df["Date"].iloc[-1], color="#555555", linestyle=":", linewidth=1.2)
ax.set_title("Future Trend Prediction - Next 30 Days")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: f"${value:,.0f}"))
ax.legend()
ax.grid(alpha=0.35)
forecast_end = forecast_df["Forecast_Close"].iloc[-1]
forecast_direction = "increase" if forecast_end >= end_price else "decrease"
add_takeaway(fig, [
    f"Last actual close: ${end_price:,.2f}",
    f"Predicted close after {forecast_days} days: ${forecast_end:,.2f} ({forecast_direction})",
])
plt.tight_layout(rect=[0, 0.16, 1, 1])
plt.savefig("data/charts/04_future_trend_prediction.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig)
print("   Saved: 04_future_trend_prediction.png")

print("\n   [Visualization Complete]")


# ============================================================
#  FINAL: INSIGHTS REPORT
# ============================================================
print("\n" + "=" * 60)
print("  TIME SERIES INSIGHTS REPORT")
print("=" * 60)

print(f"""
  TREND ANALYSIS
  --------------
  Start Price      : ${start_price:,.2f}
  End Price        : ${end_price:,.2f}
  Overall Movement : {'Upward' if overall_change >= 0 else 'Downward'}
  Overall Change   : ${overall_change:,.2f} ({overall_change_pct:.2f}%)

  PRICE EXTREMES
  --------------
  Highest Close    : ${highest_price:,.2f} on {highest_date.date()}
  Lowest Close     : ${lowest_price:,.2f} on {lowest_date.date()}

  SEASONALITY
  -----------
  Highest Avg Month: {best_month} (${seasonality.max():,.2f})
  Lowest Avg Month : {worst_month} (${seasonality.min():,.2f})

  FUTURE TREND PREDICTION
  -----------------------
  Next {forecast_days} days forecast direction: {forecast_direction}
  Predicted close after {forecast_days} days: ${forecast_end:,.2f}

  Note: This is a simple educational forecast for internship analysis,
  not financial advice.
""")

print("=" * 60)
print("  4 charts saved in: data/charts/")
print("  Task 7 - Time Series Analysis Complete!")
print("=" * 60)
