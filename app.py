import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📈 SMA Crossover Backtester")

# User inputs
symbol = st.text_input("Enter Ticker", value="TATAMOTORS.NS")
start = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end = st.date_input("End Date", value=pd.to_datetime("2024-01-01"))

fast = st.number_input("Fast SMA window", min_value=2, value=5)
slow = st.number_input("Slow SMA window", min_value=fast+1, value=15)

if st.button("Run Backtest"):
    try:
        df = yf.download(symbol, start=start, end=end)[['Adj Close']].rename(columns={"Adj Close": "Close"})
        if df.empty:
            st.error("No data returned. Check the ticker or date range.")
        else:
            # Compute indicators
            df[f'SMA_{fast}'] = df['Close'].rolling(window=fast).mean()
            df[f'SMA_{slow}'] = df['Close'].rolling(window=slow).mean()
            df['Signal'] = (df[f'SMA_{fast}'] > df[f'SMA_{slow}']).astype(int)
            df['Position'] = df['Signal'].diff()
            df.dropna(inplace=True)

            st.success(f"Data & signals calculated for {symbol}")

            # Show chart
            st.line_chart(df[['Close', f'SMA_{fast}', f'SMA_{slow}']])

            # Show buy/sell markers in matplotlib
            st.subheader("Buy/Sell Signals")
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.plot(df['Close'], label='Close Price', alpha=0.5)
            ax.plot(df[f'SMA_{fast}'], label=f'{fast}-day SMA', linestyle='--')
            ax.plot(df[f'SMA_{slow}'], label=f'{slow}-day SMA', linestyle='--')

            ax.scatter(df[df['Position'] == 1].index, df['Close'][df['Position'] == 1],
                       marker='^', color='green', label='Buy Signal', s=100)
            ax.scatter(df[df['Position'] == -1].index, df['Close'][df['Position'] == -1],
                       marker='v', color='red', label='Sell Signal', s=100)

            ax.set_title(f"SMA Crossover Strategy – {symbol}")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")

