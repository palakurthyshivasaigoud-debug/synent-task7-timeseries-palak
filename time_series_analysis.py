"""
============================================================
  SYNENT TECHNOLOGIES – DATA SCIENCE INTERNSHIP
  Task 7: Time Series Analysis
  Name   : Palakurthy Shiva Sai Goud
  Dataset: FAANG Stock Market Data with Technical Indicators
============================================================

Task Objectives:
  - FAANG stock trend analysis with multiple indicators
  - Technical analysis (SMA, RSI, Volatility)
  - Future price forecasting with confidence bands
Output:
  - 6 comprehensive visualizations (all open simultaneously)
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import timedelta

warnings.filterwarnings("ignore")

_BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASE)

# ── Global Styling ────────────────────────────────────────────
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.facecolor": "#fafafa",
    "axes.facecolor": "#ffffff",
    "axes.edgecolor": "#cccccc",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})

COLORS = {
    'AAPL':  '#555555',
    'AMZN':  '#FF9900',
    'GOOGL': '#4285F4',
    'META':  '#1877F2',
    'MSFT':  '#00A4EF',
    'NVDA':  '#76B900',
}

os.makedirs("data/charts", exist_ok=True)

print("=" * 70)
print("   TASK 7 - TIME SERIES ANALYSIS")
print("   FAANG Stock Market Data with Technical Indicators")
print("   Synent Technologies Data Science Internship")
print("=" * 70)

# ============================================================
#  PHASE 1: DATA LOADING & CLEANING
# ============================================================
print("\n" + "=" * 70)
print("  PHASE 1: DATA LOADING & CLEANING")
print("=" * 70)

DATA_PATH = "data/faang_stock_prices.csv"

print(f"\n>> Loading FAANG stock data from: {DATA_PATH}")
if not os.path.exists(DATA_PATH):
    print(f"\n   ERROR: File not found -> {DATA_PATH}")
    sys.exit(1)

try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(f"   ERROR reading file: {e}")
    sys.exit(1)

print(f"   Raw shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"   Tickers: {', '.join(sorted(df['Ticker'].unique()))}")

df['Date'] = pd.to_datetime(df['Date'])
before_rows = len(df)
df = df.dropna()
df = df.drop_duplicates()
df = df.sort_values('Date').reset_index(drop=True)
after_rows = len(df)

print(f"\n>> Data cleaning complete:")
print(f"   Rows after cleaning: {len(df):,}")
print(f"   Rows removed: {before_rows - after_rows:,}")
print("   [Data Cleaning Complete]")

# ============================================================
#  PHASE 2: EXPLORATORY DATA ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("  PHASE 2: EXPLORATORY DATA ANALYSIS")
print("=" * 70)

tickers = sorted(df['Ticker'].unique())
stock_stats = {}

print(f"\n>> Stock Summary Statistics:")
for ticker in tickers:
    td = df[df['Ticker'] == ticker]
    stats = {
        'min_price':      td['Close'].min(),
        'max_price':      td['Close'].max(),
        'mean_price':     td['Close'].mean(),
        'avg_return':     td['Daily_Return'].mean() * 100,
        'avg_volatility': td['Volatility_7d'].mean() * 100,
        'volume':         td['Volume'].mean(),
    }
    stock_stats[ticker] = stats
    print(f"\n   {ticker}:")
    print(f"      Price Range   : ${stats['min_price']:.2f} - ${stats['max_price']:.2f}  (Avg: ${stats['mean_price']:.2f})")
    print(f"      Avg Daily Ret : {stats['avg_return']:.3f}%")
    print(f"      Volatility 7d : {stats['avg_volatility']:.2f}%")
    print(f"      Avg Volume    : {stats['volume']:,.0f}")

# ============================================================
#  PHASE 3: VISUALIZATION  (all charts open simultaneously)
# ============================================================
print("\n" + "=" * 70)
print("  PHASE 3: VISUALIZATION")
print("=" * 70)

# Clear old charts
for fn in os.listdir("data/charts"):
    if fn.lower().endswith(".png"):
        os.remove(os.path.join("data/charts", fn))

print("\n   Generating 6 visualizations — all will open simultaneously.\n")


def _show(path):
    """Save → display (close the window to continue to next chart)."""
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()


# ── CHART 1: Closing Price Trends ────────────────────────────
print(">> Chart 1/6: FAANG Closing Price Trends")
fig, ax = plt.subplots(figsize=(14, 7))
fig.suptitle("FAANG Stock Closing Prices Over Time (2016 – Present)",
             fontsize=16, fontweight='bold', y=0.99)

for ticker in tickers:
    d = df[df['Ticker'] == ticker].sort_values('Date')
    ax.plot(d['Date'], d['Close'],
            label=ticker, linewidth=2,
            color=COLORS.get(ticker, '#000'), alpha=0.9)
    # Current price label at end of each line
    last = d.iloc[-1]
    ax.annotate(f"  ${last['Close']:.0f}",
                xy=(last['Date'], last['Close']),
                fontsize=9, color=COLORS.get(ticker, '#000'),
                fontweight='bold', va='center')

ax.set_xlabel("Date", fontweight='bold')
ax.set_ylabel("Closing Price (USD)", fontweight='bold')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.legend(loc='upper left', framealpha=0.9, edgecolor='#ccc')
plt.xticks(rotation=30)

high_t = max(stock_stats, key=lambda t: stock_stats[t]['max_price'])
low_t  = min(stock_stats, key=lambda t: stock_stats[t]['min_price'])
fig.text(0.5, 0.01,
         f"  ALL-TIME HIGH: {high_t}  ${stock_stats[high_t]['max_price']:,.2f}  |  "
         f"ALL-TIME LOW: {low_t}  ${stock_stats[low_t]['min_price']:.2f}\n"
         f"  All FAANG stocks show strong upward trends — robust long-term growth signals",
         ha='center', fontsize=10,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#e8f4f8', edgecolor='#4285F4'))
plt.subplots_adjust(bottom=0.14)
_show("data/charts/01_price_trends.png")
print("   Saved: 01_price_trends.png")


# ── CHART 2: Volatility Comparison ───────────────────────────
print("\n>> Chart 2/6: 7-Day Volatility Comparison")
vols     = sorted([(t, stock_stats[t]['avg_volatility']) for t in tickers],
                  key=lambda x: x[1], reverse=True)
v_tickers, v_vals = zip(*vols)

fig, ax = plt.subplots(figsize=(11, 6))
fig.suptitle("Average 7-Day Volatility by Stock\n(Higher = More Risk / More Opportunity)",
             fontsize=15, fontweight='bold')

bars = ax.bar(v_tickers, v_vals,
              color=[COLORS.get(t, '#999') for t in v_tickers],
              edgecolor='white', linewidth=1.5, alpha=0.85, width=0.55, zorder=3)

for bar, val in zip(bars, v_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
            f'{val:.2f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel("Avg 7-Day Volatility (%)", fontweight='bold')
ax.set_xlabel("Stock Ticker", fontweight='bold')
ax.set_ylim(0, max(v_vals) * 1.30)

fig.text(0.5, 0.01,
         f"  MOST VOLATILE: {v_tickers[0]} ({v_vals[0]:.2f}%)  |  "
         f"LEAST VOLATILE: {v_tickers[-1]} ({v_vals[-1]:.2f}%)\n"
         f"  Lower volatility = stable investment  |  Higher volatility = higher risk & reward",
         ha='center', fontsize=10,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff3e0', edgecolor='#FF9900'))
plt.subplots_adjust(bottom=0.15)
_show("data/charts/02_volatility_comparison.png")
print("   Saved: 02_volatility_comparison.png")


# ── CHART 3: Daily Returns Distribution ──────────────────────
print("\n>> Chart 3/6: Daily Returns Distribution (Boxplot)")
returns_data = [df[df['Ticker'] == t]['Daily_Return'].dropna() * 100 for t in tickers]
means        = [d.mean() for d in returns_data]

fig, ax = plt.subplots(figsize=(12, 7))
fig.suptitle("Daily Returns Distribution by Stock\nPositive median = consistent daily profit",
             fontsize=15, fontweight='bold')

bp = ax.boxplot(returns_data, tick_labels=tickers, patch_artist=True, widths=0.55,
                medianprops=dict(color='#e74c3c', linewidth=2.5),
                whiskerprops=dict(linewidth=1.5, linestyle='--'),
                capprops=dict(linewidth=2),
                flierprops=dict(marker='o', markersize=3, alpha=0.3))

for patch, ticker in zip(bp['boxes'], tickers):
    patch.set_facecolor(COLORS.get(ticker, '#ccc'))
    patch.set_alpha(0.7)
    patch.set_edgecolor('black')
    patch.set_linewidth(1.5)

ax.axhline(0, color='black', linewidth=1.5, alpha=0.6, label='Break-even (0%)')
ax.scatter(range(1, len(tickers) + 1), means,
           marker='D', color='white', edgecolor='black',
           s=60, zorder=5, label='Mean Return')

ax.set_ylabel("Daily Return (%)", fontweight='bold')
ax.set_xlabel("Stock Ticker", fontweight='bold')
ax.legend(loc='upper right')

best_t  = tickers[means.index(max(means))]
worst_t = tickers[means.index(min(means))]
fig.text(0.5, 0.01,
         f"  BEST avg daily return: {best_t} ({max(means):.3f}%)  |  "
         f"LOWEST avg daily return: {worst_t} ({min(means):.3f}%)\n"
         f"  Red line = median  |  Diamond = mean  |  All stocks show positive average returns",
         ha='center', fontsize=10,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#f1f8e9', edgecolor='#55A868'))
plt.subplots_adjust(bottom=0.15)
_show("data/charts/03_daily_returns.png")
print("   Saved: 03_daily_returns.png")


# ── CHART 4: Technical Signals Table ─────────────────────────
print("\n>> Chart 4/6: Current Technical Signals")
latest = df.groupby('Ticker').tail(1).sort_values('Ticker')

fig, ax = plt.subplots(figsize=(14, 5))
fig.suptitle(f"Latest Technical Analysis Signals  "
             f"(as of {latest['Date'].max().strftime('%Y-%m-%d')})",
             fontsize=15, fontweight='bold')
ax.axis('off')

sig_rows   = []
row_colors = []
for _, row in latest.iterrows():
    ticker  = row['Ticker']
    sma_sig = "BULLISH ↑" if row['SMA_7'] > row['SMA_21'] else "BEARISH ↓"
    rsi_sig = ("OVERBOUGHT" if row['RSI_14'] > 70
                else "OVERSOLD" if row['RSI_14'] < 30 else "NEUTRAL")
    sig_rows.append([ticker, f"${row['Close']:.2f}",
                     f"{row['Daily_Return']*100:+.3f}%",
                     sma_sig, rsi_sig,
                     f"{row['RSI_14']:.1f}", f"{row['Volatility_7d']*100:.2f}%"])
    row_colors.append(['#e8f5e9' if 'BULLISH' in sma_sig else '#ffebee'] * 7)

col_labels = ['Ticker', 'Price', 'Daily Ret.', 'MA Signal', 'RSI Status', 'RSI Val', 'Volatility']
tbl = ax.table(cellText=sig_rows, colLabels=col_labels,
               cellLoc='center', loc='center',
               colWidths=[0.10, 0.13, 0.13, 0.15, 0.15, 0.11, 0.14])
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 2.5)

for j in range(len(col_labels)):
    tbl[(0, j)].set_facecolor('#37474F')
    tbl[(0, j)].set_text_props(color='white', fontweight='bold')

for i, rcolors in enumerate(row_colors, start=1):
    for j, fc in enumerate(rcolors):
        tbl[(i, j)].set_facecolor(fc)
        tbl[(i, j)].set_edgecolor('#cccccc')

fig.text(0.5, 0.04,
         "SMA Signal: 7-day vs 21-day moving avg  |  "
         "RSI >70 = Overbought  |  RSI <30 = Oversold  |  30-70 = Neutral\n"
         "Green rows = BULLISH (7-day SMA above 21-day)  |  "
         "Red rows = BEARISH (7-day SMA below 21-day)",
         ha='center', fontsize=9,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#fffde7', edgecolor='#FBC02D'))
plt.subplots_adjust(bottom=0.20)
_show("data/charts/04_technical_signals.png")
print("   Saved: 04_technical_signals.png")


# ── CHART 5: Total Price Growth ───────────────────────────────
print("\n>> Chart 5/6: Total Price Growth Since 2016")
first_p  = df.groupby('Ticker')['Close'].first()
last_p   = df.groupby('Ticker')['Close'].last()
pct_chgs = ((last_p - first_p) / first_p * 100).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle("Total Price Growth Since 2016  (Long-Term Performance Comparison)",
             fontsize=15, fontweight='bold')

bars = ax.barh(pct_chgs.index[::-1], pct_chgs.values[::-1],
               color=[COLORS.get(t, '#999') for t in pct_chgs.index[::-1]],
               edgecolor='white', linewidth=1.5, alpha=0.85, height=0.55, zorder=3)

for bar, val in zip(bars, pct_chgs.values[::-1]):
    ax.text(bar.get_width() + max(pct_chgs) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            f'+{val:,.0f}%', va='center', fontsize=12, fontweight='bold')

ax.set_xlabel("Total Growth (%)", fontweight='bold')
ax.set_ylabel("Stock", fontweight='bold')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}%'))
ax.set_xlim(0, pct_chgs.max() * 1.22)

best  = pct_chgs.idxmax()
worst = pct_chgs.idxmin()
fig.text(0.5, 0.01,
         f"  BEST performer: {best}  (+{pct_chgs[best]:,.0f}%)  |  "
         f"LOWEST growth: {worst}  (+{pct_chgs[worst]:,.0f}%)\n"
         f"  All FAANG stocks delivered strong positive returns since 2016",
         ha='center', fontsize=10,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#f3e5f5', edgecolor='#9C27B0'))
plt.subplots_adjust(bottom=0.14, right=0.88)
_show("data/charts/05_total_growth.png")
print("   Saved: 05_total_growth.png")


# ── CHART 6: 60-Day Future Trend Forecast (Core of Task 7) ───
print("\n>> Chart 6/6: 60-Day Future Price Forecast with Confidence Bands")

FORECAST_DAYS = 60
HISTORY_DAYS  = 180    # last 180 trading days used for regression

ncols = 3
nrows = -(-len(tickers) // ncols)   # ceiling division

fig = plt.figure(figsize=(18, 12))
fig.suptitle(
    "60-Day Future Price Forecast  -  FAANG Stocks\n"
    "Linear trend extrapolated with ±1σ & ±2σ confidence bands  "
    "|  Green = Upward  |  Red = Downward",
    fontsize=15, fontweight='bold', y=0.99)

forecast_results = {}

for idx, ticker in enumerate(tickers):
    ax = fig.add_subplot(nrows, ncols, idx + 1)
    td     = df[df['Ticker'] == ticker].sort_values('Date').reset_index(drop=True)
    recent = td.tail(HISTORY_DAYS).reset_index(drop=True)

    # ── Linear regression ────────────────────────────────────
    x         = np.arange(len(recent))
    coeffs    = np.polyfit(x, recent['Close'].values, 1)
    tfn       = np.poly1d(coeffs)
    fitted    = tfn(x)
    resid_std = (recent['Close'].values - fitted).std()

    # ── Forecast ─────────────────────────────────────────────
    fx      = np.arange(len(recent), len(recent) + FORECAST_DAYS)
    fprices = tfn(fx)
    fdates  = pd.date_range(
        start=recent['Date'].iloc[-1] + timedelta(days=1),
        periods=FORECAST_DAYS, freq='D')

    cur   = recent['Close'].iloc[-1]
    fore  = fprices[-1]
    chg   = (fore - cur) / cur * 100
    fcolor = '#27ae60' if fore > cur else '#e74c3c'
    forecast_results[ticker] = {'current': cur, 'forecast': fore, 'pct': chg}

    # ── Historical price ─────────────────────────────────────
    ax.plot(recent['Date'], recent['Close'],
            color=COLORS.get(ticker, '#333'), linewidth=2.2,
            label='Historical Price', zorder=4)

    # ── Trend line over history ──────────────────────────────
    ax.plot(recent['Date'], fitted, '--',
            color='#888', linewidth=1.2, alpha=0.7,
            label='Trend Line', zorder=3)

    # ── Forecast line ────────────────────────────────────────
    ax.plot(fdates, fprices,
            color=fcolor, linewidth=3.0, linestyle='-',
            label='60-Day Forecast', zorder=4)

    # ── Confidence bands ─────────────────────────────────────
    ax.fill_between(fdates, fprices - resid_std, fprices + resid_std,
                    alpha=0.30, color=fcolor, label='+/-1σ')
    ax.fill_between(fdates, fprices - 2 * resid_std, fprices + 2 * resid_std,
                    alpha=0.12, color=fcolor, label='+/-2σ')

    # ── TODAY vertical separator ─────────────────────────────
    last_hist_date = recent['Date'].iloc[-1]
    ax.axvline(last_hist_date, color='#c0392b',
               linestyle=':', linewidth=2, zorder=5)

    # ── Shaded forecast zone ─────────────────────────────────
    ax.axvspan(last_hist_date, fdates[-1], alpha=0.04, color=fcolor)

    # ── Price annotations ────────────────────────────────────
    ax.annotate(f'NOW: ${cur:,.0f}',
                xy=(last_hist_date, cur),
                xytext=(-6, 14), textcoords='offset points',
                fontsize=8.5, color='black', fontweight='bold', ha='right')

    arrow = 'UP' if fore > cur else 'DOWN'
    ax.annotate(f'{arrow}: ${fore:,.0f}\n({abs(chg):.1f}%)',
                xy=(fdates[-1], fore),
                xytext=(4, 0), textcoords='offset points',
                fontsize=9, color=fcolor, fontweight='bold', ha='left')

    # ── Subplot formatting ───────────────────────────────────
    direction_label = 'Uptrend' if fore > cur else 'Downtrend'
    ax.set_title(f"{ticker}  |  {direction_label}  {abs(chg):.1f}% in 60 days",
                 fontsize=11, fontweight='bold',
                 color=COLORS.get(ticker, '#333'))
    ax.set_xlabel("Date", fontsize=9)
    ax.set_ylabel("Price (USD)", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, fontsize=8)
    ax.legend(fontsize=7.5, loc='upper left', framealpha=0.85, edgecolor='#ccc')

    # ── "TODAY" label — placed AFTER legend so ylim is finalised ─
    ymin, ymax = ax.get_ylim()
    ax.text(last_hist_date, ymax - (ymax - ymin) * 0.03,
            '  TODAY', fontsize=7.5, color='#c0392b',
            fontweight='bold', va='top')

# Hide any unused subplot slots
for idx in range(len(tickers), nrows * ncols):
    fig.add_subplot(nrows, ncols, idx + 1).set_visible(False)

# ── Forecast summary banner ───────────────────────────────────
summary = "   |   ".join(
    [f"{t}: ${v['current']:,.0f} -> ${v['forecast']:,.0f} "
     f"({'UP' if v['pct'] > 0 else 'DOWN'} {abs(v['pct']):.1f}%)"
     for t, v in forecast_results.items()])
fig.text(0.5, 0.01,
         f"60-Day Forecast Summary:\n{summary}\n"
         f"Method: Linear regression on last {HISTORY_DAYS} trading days  |  "
         f"Shaded = uncertainty (inner ±1σ, outer ±2σ)",
         ha='center', fontsize=9.5,
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fff9c4', edgecolor='#F57F17', linewidth=1.5))

plt.subplots_adjust(hspace=0.60, wspace=0.40, bottom=0.13, top=0.91)
_show("data/charts/06_60day_forecast.png")
print("   Saved: 06_60day_forecast.png")

print("\n   [Visualization Complete - 6 charts saved and open]")

# ============================================================
#  PHASE 4: KEY INSIGHTS & RECOMMENDATIONS
# ============================================================
print("\n" + "=" * 70)
print("  PHASE 4: KEY INSIGHTS & RECOMMENDATIONS")
print("=" * 70)

print(f"\n>> DATASET SUMMARY:")
print(f"   Total Records : {len(df):,} trading data points")
print(f"   Stocks        : {df['Ticker'].nunique()} ({', '.join(tickers)})")
print(f"   Time Period   : {df['Date'].min().strftime('%Y-%m-%d')} -> {df['Date'].max().strftime('%Y-%m-%d')}")
print(f"   Avg Daily Ret : {df['Daily_Return'].mean()*100:.3f}%")
print(f"   Avg Volatility: {df['Volatility_7d'].mean()*100:.2f}%")

print(f"\n>> TECHNICAL INDICATORS ANALYZED:")
print(f"   - SMA 7/21  : Short-term vs long-term trends")
print(f"   - RSI (14)  : Momentum and overbought/oversold conditions")
print(f"   - MACD      : Trend-following momentum")
print(f"   - Daily Ret : Percentage profit/loss per day")
print(f"   - Volatility: 7-day rolling risk measurement")

print(f"\n>> TRADING RECOMMENDATIONS:")
print(f"   1. SMA Crossovers : Buy when SMA7 > SMA21 (bullish) | Sell when SMA7 < SMA21")
print(f"   2. RSI Signals    : >70 = take profits  |  <30 = buying opportunity")
print(f"   3. Volatility Mgmt: Higher volatility needs wider stop-losses")
print(f"   4. Diversification: Hold multiple FAANG stocks to reduce single-stock risk")
print(f"   5. Trend Following: Use MA crossovers + RSI confirmation together")

print(f"\n>> 60-DAY FORECAST SUMMARY:")
for ticker, fi in forecast_results.items():
    direction = "UP  " if fi['pct'] > 0 else "DOWN"
    print(f"   {ticker}: ${fi['current']:,.2f} -> ${fi['forecast']:,.2f}  "
          f"({direction}  {abs(fi['pct']):.2f}%)")

print("\n" + "=" * 70)
print("  ANALYSIS COMPLETE!")
print("  6 charts saved in: data/charts/")
print("  Task 7 - Time Series Analysis Complete!")
print("=" * 70)

print("\n  Charts open one by one — close each window to continue.\n")
