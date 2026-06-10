# synent-task7-timeseries-palak

## Task 7: Time Series Analysis

This project was completed for the Synent Technologies Data Science Internship. It analyzes CIPLA stock price data to understand time-based trends, detect seasonality patterns, and forecast future values using moving average analysis and linear trend modeling.

## Problem Statement

Financial analysts need to understand stock price movements over time to identify trends and make informed predictions. In this project, I analyzed historical CIPLA stock closing prices to identify long-term trends, seasonal patterns, and short-term fluctuations using moving average indicators and time-based aggregations.

## Dataset

The CIPLA stock historical data can be downloaded from:
- **Kaggle**: [Indian Stock Market Data with Technical Analysis](https://www.kaggle.com/datasets/rohanrao/nse-stock-market-data)

Local copy:
- `CIPLA.csv` - Contains historical CIPLA stock prices from NSE (National Stock Exchange)

Important columns:
- `Date`: Trading date
- `Close`: Closing price
- `High`: Daily high
- `Low`: Daily low
- `Open`: Opening price

## Approach

1. Loaded the stock price dataset and converted date columns to datetime format.
2. Removed missing values and duplicates, sorted chronologically.
3. Calculated daily returns and moving averages (20-day and 50-day MA).
4. Created time-based aggregations: monthly and yearly averages.
5. Analyzed trend direction and identified best/worst performing years.
6. Detected seasonality by comparing average prices across months.
7. Built a linear regression model on recent prices to forecast the next 30 days.
8. Generated visualizations with trend signals and prediction intervals.

## Key Results

- **Overall Price Movement**: Stock showed consistent movement patterns across the analysis period
- **Trend Analysis**: Identified best and worst performing years with year-over-year comparisons
- **Moving Average Signals**: 20-day vs 50-day MA crossovers indicate bullish or bearish trends
- **Seasonality**: Detected months with highest and lowest average closing prices
- **Volatility**: Calculated daily return volatility for risk assessment
- **30-Day Forecast**: Linear trend model predicts future price movements with confidence intervals

## Visualizations

Charts are saved in `data/charts/`.

| Chart | Description |
|-------|-------------|
| `01_closing_price_trend.png` | Historical closing price with highest/lowest extremes |
| `02_moving_averages.png` | 20-day and 50-day MA trends with bullish/bearish signals |
| `03_monthly_seasonality.png` | Average close price by month showing seasonal patterns |
| `04_future_trend_prediction.png` | 30-day linear forecast with prediction range |

## How to Run

```bash
pip install -r requirements.txt
python time_series_analysis.py
```

## Repository Structure

```text
synent-task7-timeseries-palak/
|-- README.md
|-- time_series_analysis.py
|-- CIPLA.csv
|-- requirements.txt
|-- data/
|   `-- charts/
`-- .gitignore
```

## Internship Requirement Mapping

| Requirement | Status |
| --- | --- |
| Trend analysis | Completed |
| Seasonality detection | Completed |
| Future value forecast (optional) | Completed |
| Meaningful visualizations | Completed |
| Time-based insights report | Completed |
| Dataset included | Completed |

## Author

Palakurthy Shiva Sai Goud

Submitted for Synent Technologies Data Science Internship - Task 7.

---

## How to Run

```bash
pip install pandas numpy matplotlib seaborn
python time_series_analysis.py
```

---

*Submitted as part of the Synent Technologies Data Science Internship Program - Task 7*
