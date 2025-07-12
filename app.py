import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📈 SMA Crossover Backtester")

symbol = st.text_input("Enter Ticker", value="TATAMOTORS.NS")
start = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end = st.date_input("End Date", value=pd.to_datetime("2024-01-01"))

if st.button("Run Backtest"):
    df = yf.download(symbol, start=start, end=end)[['Close']]
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_15'] = df['Close'].rolling(window=15).mean()
    df['Signal'] = (df['SMA_5'] > df['SMA_15']).astype(int)
    df['Position'] = df['Signal'].diff()
    st.line_chart(df[['Close', 'SMA_5', 'SMA_15']])
