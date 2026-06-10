# synent-task7-timeseries-palak

## Task 7: Time Series Analysis

This project was completed for the Synent Technologies Data Science Internship. It analyzes FAANG (Facebook/Meta, Apple, Amazon, Netflix, Google/Alphabet) stock market data to identify trends, track technical indicators, and generate trading signals using moving averages, RSI, and other technical analysis tools.

## Problem Statement

Stock market analysts need comprehensive technical analysis tools to identify trading opportunities and manage risk. In this project, I analyzed 14,964+ records of FAANG stock prices with pre-calculated technical indicators to identify trend signals (moving average crossovers), momentum conditions (RSI levels), and volatility patterns to inform investment decisions.

## Dataset

The FAANG stock market data can be downloaded from:
- **Kaggle**: [Stock Price Dataset FAANG+](https://www.kaggle.com/datasets/vishardmehta/faang-stock-market-data-with-technical-indicators)

Local copy:
- `faang_stock_prices.csv` - Contains historical FAANG stock prices with technical indicators

Important columns:
- `Date`: Trading date
- `Ticker`: Stock symbol (AAPL, AMZN, GOOGL, META, MSFT)
- `Close`: Closing price
- `Open`, `High`, `Low`: OHLC data
- `Volume`: Trading volume
- `SMA_7`, `SMA_21`: Simple Moving Averages
- `EMA_12`, `EMA_26`: Exponential Moving Averages
- `RSI_14`: Relative Strength Index
- `MACD`: Moving Average Convergence Divergence
- `Daily_Return`: Daily percentage return
- `Volatility_7d`: 7-day rolling volatility

## Approach

1. **Data Loading & Cleaning**: Load 14,964 FAANG trading records and handle missing/duplicate values
2. **Exploratory Data Analysis**: Summary statistics for each stock (AAPL, AMZN, GOOGL, META, MSFT)
3. **Technical Indicator Analysis**: Analyze SMA, EMA, RSI, MACD, Bollinger Bands
4. **Visualization**: Generate 5 comprehensive charts with HIGH/LOW tracking:
   - Closing Price Trends (multi-stock comparison)
   - Moving Average Crossover Analysis (7-day vs 21-day)
   - 7-Day Volatility Trends (risk assessment)
   - Daily Returns Distribution (performance variance)
   - RSI Technical Indicator (overbought/oversold signals)
5. **Insights & Recommendations**: Market signals and trading strategy suggestions

## Key Results & Insights

### Dataset Characteristics
- **Records**: 14,964 trading data points across 5 FAANG stocks
- **Time Period**: Feb 2016 to present
- **Stocks Analyzed**: AAPL, AMZN, GOOGL, META, MSFT
- **Technical Features**: 19 indicators (SMA, EMA, RSI, MACD, Bollinger Bands, etc.)

### Performance Metrics
- **Average Daily Return**: ~0.05% across all stocks
- **Average Volatility**: ~1.5-2% (7-day rolling)
- **Price Range**: See 01_closing_price_trends.png for stock-specific highs/lows

### Technical Analysis Findings
- **SMA Crossovers**: 7-day > 21-day indicates BULLISH trends; 7-day < 21-day indicates BEARISH
- **RSI Signals**: RSI >70 = Overbought conditions (potential pullback); RSI <30 = Oversold (potential bounce)
- **Volatility Pattern**: Higher volatility during market uncertainty and earnings announcements
- **Returns Distribution**: All stocks show positive average returns with varying risk profiles

### Key Observations
1. All FAANG stocks trend upward over the entire analyzed period
2. AMZN and MSFT demonstrate relatively stable growth with lower volatility
3. META shows higher volatility compared to other FAANG components
4. Moving average crossovers provide reliable entry and exit signals
5. RSI effectively identifies overbought/oversold trading opportunities

## Visualizations

5 key visualizations with detailed HIGH/LOW tracking saved in `data/charts/`:

| Chart | Description |
|-------|-------------|
| `01_closing_price_trends.png` | **Closing Price Trends**: HIGH/LOW by stock showing multi-year trends for AAPL, AMZN, GOOGL, META, MSFT |
| `02_moving_averages.png` | **Moving Average Crossover**: 7-day vs 21-day SMA signals (HIGH: 7>21 Bullish, LOW: 7<21 Bearish) |
| `03_volatility_trend.png` | **Volatility Analysis**: 7-day rolling volatility (HIGH: peak volatility events, LOW: stable periods) |
| `04_daily_returns.png` | **Daily Returns Distribution**: Performance variance by stock (HIGH: best avg return, LOW: lowest return) |
| `05_rsi_analysis.png` | **RSI Technical Indicator**: Overbought/Oversold signals (HIGH: RSI>70, LOW: RSI<30) |

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

| Requirement | Status | Details |
| --- | --- | --- |
| Multi-stock time series analysis | ✓ Completed | 5 FAANG stocks with 14,964+ records |
| Technical indicator analysis | ✓ Completed | SMA, EMA, RSI, MACD, Bollinger Bands |
| Trend identification | ✓ Completed | Moving average crossovers and directionality |
| Volatility tracking | ✓ Completed | 7-day rolling volatility with HIGH/LOW analysis |
| 5 meaningful visualizations | ✓ Completed | Each with HIGH/LOW statistical annotations |
| Time-based insights report | ✓ Completed | Trading signals and strategy recommendations |
| Kaggle dataset included | ✓ Completed | FAANG stock market data with indicators |

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
