# Simple Moving Average (SMA) Crossover Backtesting in Python
This project implements a straightforward backtesting framework for a simple moving average (SMA) crossover trading strategy using Python and Pandas.

Deployed with StreamLit- https://backtesting-ezi3yt44q5da2siz2eu4c6.streamlit.app/

It allows you to:
1. Fetch and clean historical stock data
2. Calculate fast and slow SMAs (e.g., 20-day and 50-day)
3. Generate buy/sell signals based on SMA crossovers
4. Simulate trading behavior with capital allocation
5. Track portfolio value over time
6. Visualize trades and portfolio performance

## Strategy Logic
Buy Signal: When the short-term SMA crosses above the long-term SMA
Sell Signal: When the short-term SMA crosses below the long-term SMA

The backtester assumes 100% capital is invested on each buy and fully liquidated on each sell (no position sizing logic yet).

## Outputs
1. Number of Buy and Sell signals

2. Final Portfolio Value

3. Line plot of: Closing prices, SMA lines, Buy/Sell signals, Portfolio value over time

## Tools & Libraries Used
1. pandas – data manipulation

2. numpy – numerical computations

3. matplotlib – visualization

4. yfinance – fetching historical stock data
