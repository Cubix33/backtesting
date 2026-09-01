import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ----- Page Config -----
st.set_page_config(page_title="TradeSight", page_icon="📈", layout="wide")

# ----- Sidebar Inputs -----
st.sidebar.title("📊 Strategy Parameters")
st.sidebar.markdown("---")

# Preset stocks grouped by market
PRESET_STOCKS = {
    "🇮🇳 NSE — Large Cap": {
        "Reliance Industries": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "Wipro": "WIPRO.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Bajaj Finance": "BAJFINANCE.NS",
        "Maruti Suzuki": "MARUTI.NS",
        "Sun Pharma": "SUNPHARMA.NS",
    },
    "🇮🇳 NSE — Mid Cap": {
        "Tata Power": "TATAPOWER.NS",
        "Zomato": "ZOMATO.NS",
        "Paytm": "PAYTM.NS",
        "Nykaa": "NYKAA.NS",
        "Delhivery": "DELHIVERY.NS",
    },
    "🇺🇸 US — Tech": {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Alphabet (Google)": "GOOGL",
        "Meta": "META",
        "Amazon": "AMZN",
        "Tesla": "TSLA",
    },
    "🇺🇸 US — Others": {
        "Berkshire Hathaway": "BRK-B",
        "JPMorgan Chase": "JPM",
        "Coca-Cola": "KO",
    },
    "✏️ Custom Symbol": {},
}

selected_group = st.sidebar.selectbox("Select Market / Group", list(PRESET_STOCKS.keys()))

if selected_group == "✏️ Custom Symbol":
    symbol = st.sidebar.text_input(
        "Enter Stock Symbol",
        placeholder="e.g. INFY.NS or AAPL",
        help="NSE India: add .NS suffix · BSE India: add .BO · US: plain ticker"
    )
    if not symbol:
        st.sidebar.info("Enter a ticker symbol above to get started.")
else:
    stock_options = PRESET_STOCKS[selected_group]
    selected_name = st.sidebar.selectbox("Select Stock", list(stock_options.keys()))
    symbol = stock_options[selected_name]
    st.sidebar.code(symbol, language=None)  # show the ticker being used

st.sidebar.markdown("---")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2024, 1, 1))
sma_short = st.sidebar.slider("Short-term SMA (days)", 3, 20, 5)
sma_long = st.sidebar.slider("Long-term SMA (days)", 10, 50, 15)

# ----- Title -----
st.title("📈 TradeSight — SMA Crossover Backtest Dashboard")
st.caption("Backtest a Simple Moving Average (SMA) crossover strategy on any stock.")

# ----- Data Download -----
@st.cache_data(show_spinner=False)
def load_data(symbol, start, end):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start, end=end, auto_adjust=True)

        if df.empty:
            return None, f"No data returned for **{symbol}**. The symbol may be delisted, incorrect, or unavailable for the selected date range."

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if 'Close' not in df.columns:
            return None, f"Could not find 'Close' price data for **{symbol}**."

        return df[['Close']], None

    except Exception as e:
        return None, f"Failed to download data for **{symbol}**: {str(e)}"

# ----- Load Data -----
if not symbol or not symbol.strip():
    st.info("👈 Select a stock from the sidebar to get started.")
    st.stop()

with st.spinner(f"Fetching data for {symbol}..."):
    df, error = load_data(symbol, start_date, end_date)

if error:
    st.error(f"⚠️ {error}")
    st.info(
        "**Troubleshooting tips:**\n"
        "- For **NSE (India)** stocks: use `SYMBOL.NS` format (e.g. `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`)\n"
        "- For **BSE (India)** stocks: use `SYMBOL.BO` format (e.g. `RELIANCE.BO`)\n"
        "- For **US** stocks: use plain ticker (e.g. `AAPL`, `TSLA`)\n"
        "- Try widening the date range — some symbols have limited historical data\n"
        "- Check [Yahoo Finance](https://finance.yahoo.com) to verify the symbol exists"
    )
    st.stop()

# ----- SMA Strategy -----
df['SMA_Short'] = df['Close'].rolling(window=sma_short).mean()
df['SMA_Long'] = df['Close'].rolling(window=sma_long).mean()
df['Signal'] = np.where(df['SMA_Short'] > df['SMA_Long'], 1, 0)
df['Position'] = df['Signal'].diff()

# Drop NaNs introduced by rolling windows
df.dropna(inplace=True)
df.reset_index(inplace=True)

# Rename index column to 'Date' if it came through as 'index' or 'Datetime'
if 'Date' not in df.columns:
    for col in ['Datetime', 'index']:
        if col in df.columns:
            df.rename(columns={col: 'Date'}, inplace=True)
            break

df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)

if df.empty:
    st.error("Not enough data after applying SMA windows. Try a wider date range or smaller SMA values.")
    st.stop()

# ----- Metrics -----
buy_signals = df[df['Position'] == 1]
sell_signals = df[df['Position'] == -1]
returns = df['Close'].pct_change().fillna(0)
strategy_returns = df['Signal'].shift(1).fillna(0) * returns
cumulative_return = (strategy_returns + 1).cumprod().iloc[-1] - 1
buy_hold_return = (df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📈 Buy Signals", f"{len(buy_signals)}")
col2.metric("📉 Sell Signals", f"{len(sell_signals)}")
col3.metric("💰 Strategy Return", f"{cumulative_return * 100:.2f}%")
col4.metric("📊 Buy & Hold Return", f"{buy_hold_return * 100:.2f}%")
st.markdown("---")

# ----- Plot -----
fig, ax = plt.subplots(figsize=(16, 7))
ax.plot(df['Date'], df['Close'], label='Close Price', alpha=0.6, linewidth=1.5)
ax.plot(df['Date'], df['SMA_Short'], label=f'{sma_short}-day SMA (Short)', linestyle='--', linewidth=1.2)
ax.plot(df['Date'], df['SMA_Long'], label=f'{sma_long}-day SMA (Long)', linestyle='--', linewidth=1.2)

# Buy/Sell Markers
if not buy_signals.empty:
    ax.scatter(buy_signals['Date'], buy_signals['Close'], label='Buy Signal', marker='^', color='green', s=120, zorder=5)
if not sell_signals.empty:
    ax.scatter(sell_signals['Date'], sell_signals['Close'], label='Sell Signal', marker='v', color='red', s=120, zorder=5)

ax.set_title(f"SMA Crossover Strategy — {symbol}", fontsize=16, fontweight='bold')
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Price", fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
fig.tight_layout()

st.pyplot(fig)

# ----- Trade Log -----
st.subheader("📜 Trade Log")
if buy_signals.empty and sell_signals.empty:
    st.info("No trades were generated. Try adjusting the SMA windows or selecting a more volatile period.")
else:
    buy_df = buy_signals[['Date', 'Close']].copy()
    buy_df['Action'] = 'Buy'
    sell_df = sell_signals[['Date', 'Close']].copy()
    sell_df['Action'] = 'Sell'
    trade_log = pd.concat([buy_df, sell_df]).sort_values('Date').reset_index(drop=True)
    trade_log['Close'] = trade_log['Close'].round(2)
    st.dataframe(trade_log, use_container_width=True)

# ----- Raw Data -----
with st.expander("🔍 View Raw Data"):
    st.dataframe(df[['Date', 'Close', 'SMA_Short', 'SMA_Long', 'Signal']].round(2), use_container_width=True)
