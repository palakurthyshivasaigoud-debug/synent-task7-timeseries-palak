# synent-task7-timeseries-palak

## Task 7: CIPLA Stock Time Series Analysis

This project was created for the Synent Technologies Data Science Internship. It studies historical stock price movement for CIPLA and explains trend, seasonality, volatility, and a simple future direction estimate.

## Problem Statement

Stock price data changes over time, so the analysis should preserve the date order and focus on movement patterns. In this task, I analyzed closing price behavior, moving averages, monthly patterns, and a simple 30-day linear forecast.

## Dataset

Source: Kaggle / historical stock price data.

Local file:

```text
CIPLA.csv
```

Main columns used:

| Column | Purpose |
| --- | --- |
| `Date` | Time index for the analysis |
| `Close` | Price column used for trend and forecast |

## Approach

1. Loaded the stock CSV file.
2. Converted the date column to datetime format.
3. Converted the closing price to numeric format.
4. Removed invalid rows and duplicate records.
5. Sorted the data by date.
6. Calculated daily return, 20-day moving average, and 50-day moving average.
7. Compared average closing prices by month for seasonality.
8. Built a simple 30-day forecast using a linear trend on recent data.

## Key Insights

- The project reports start price, end price, overall movement, highest close, and lowest close.
- Moving averages are used to compare short-term and longer-term price direction.
- Monthly averages help identify repeated seasonal patterns.
- The forecast is included only as an educational trend estimate, not financial advice.

## Visualizations

Charts are saved in `data/charts/`.

| Chart | Description |
| --- | --- |
| `01_closing_price_trend.png` | Closing price over time |
| `02_moving_averages.png` | Close price with 20-day and 50-day moving averages |
| `03_monthly_seasonality.png` | Average close price by month |
| `04_future_trend_prediction.png` | Simple 30-day forecast |

## How to Run

```bash
pip install -r requirements.txt
python time_series_analysis.py
```

## Repository Structure

```text
synent-task7-timeseries-palak/
|-- time_series_analysis.py
|-- CIPLA.csv
|-- README.md
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
| Optional forecasting | Completed |
| Time-based visual insights | Completed |
| Dataset included | Completed |

## Author

Palak

Submitted for Synent Technologies Data Science Internship - Task 7.
