import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ----- Sidebar Inputs -----
st.sidebar.title("📊 Strategy Parameters")
symbol = st.sidebar.text_input("Stock Symbol (e.g. TATAMOTORS.NS)", "TATAMOTORS.NS")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2024, 1, 1))
sma_short = st.sidebar.slider("Short-term SMA", 3, 20, 5)
sma_long = st.sidebar.slider("Long-term SMA", 10, 50, 15)

# ----- Title -----
st.title("💹 SMA Crossover Backtest Dashboard")
st.caption("Built with ❤️ using Streamlit")

# ----- Data Download -----
@st.cache_data
def load_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[['Close']]

df = load_data(symbol, start_date, end_date)

if df.empty:
    st.error("No data found. Try a different symbol or date range.")
    st.stop()

# ----- SMA Strategy -----
df['SMA_Short'] = df['Close'].rolling(window=sma_short).mean()
df['SMA_Long'] = df['Close'].rolling(window=sma_long).mean()
df['Signal'] = np.where(df['SMA_Short'] > df['SMA_Long'], 1, 0)
df['Position'] = df['Signal'].diff()

# Drop NaNs
df.dropna(inplace=True)
df.reset_index(inplace=True)

# ----- Metrics -----
buy_signals = df[df['Position'] == 1]
sell_signals = df[df['Position'] == -1]
returns = df['Close'].pct_change().fillna(0)
strategy_returns = df['Signal'].shift(1) * returns
cumulative_return = (strategy_returns + 1).cumprod().iloc[-1] - 1

col1, col2, col3 = st.columns(3)
col1.metric("📈 Buy Signals", f"{len(buy_signals)}")
col2.metric("📉 Sell Signals", f"{len(sell_signals)}")
col3.metric("💰 Total Return", f"{cumulative_return*100:.2f}%")

# ----- Plot -----
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(df['Date'], df['Close'], label='Close Price', alpha=0.5)
ax.plot(df['Date'], df['SMA_Short'], label=f'{sma_short}-day SMA', linestyle='--')
ax.plot(df['Date'], df['SMA_Long'], label=f'{sma_long}-day SMA', linestyle='--')

# Buy/Sell Markers
ax.scatter(buy_signals['Date'], buy_signals['Close'], label='Buy', marker='^', color='green', s=100)
ax.scatter(sell_signals['Date'], sell_signals['Close'], label='Sell', marker='v', color='red', s=100)

ax.set_title(f"SMA Crossover Strategy for {symbol}", fontsize=18)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ----- Trade Log -----
st.subheader("📜 Trade Log")
trade_log = pd.concat([buy_signals[['Date', 'Close']], sell_signals[['Date', 'Close']]])
trade_log['Action'] = ['Buy'] * len(buy_signals) + ['Sell'] * len(sell_signals)
trade_log.sort_values('Date', inplace=True)
trade_log.reset_index(drop=True, inplace=True)
st.dataframe(trade_log, use_container_width=True)
