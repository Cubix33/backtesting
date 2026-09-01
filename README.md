# 📈 TradeSight — SMA Crossover Backtesting Dashboard

> A Streamlit web app to backtest a Simple Moving Average (SMA) crossover trading strategy on any stock — Indian (NSE/BSE) or US.

🚀 **Live Demo:** https://backtesting-ezi3yt44q5da2siz2eu4c6.streamlit.app/

---

## 🧠 What Is This Project?

**TradeSight** is a stock market backtesting tool. The idea is simple:

> *"If I had used this trading strategy in the past, how much money would I have made (or lost)?"*

It does this using a classic strategy called **SMA Crossover**, which uses two moving averages of a stock's price to decide when to buy and sell.

---

## 📖 What Is Backtesting?

Backtesting means **testing a trading strategy on historical data** to see how it would have performed — before risking real money on it. It's a standard technique used by quants and algorithmic traders.

---

## 📐 Strategy: SMA Crossover

A **Simple Moving Average (SMA)** smooths out a stock's price over a window of N days to reduce noise.

This app uses **two SMAs**:

| SMA | Default | Purpose |
|-----|---------|---------|
| Short-term SMA | 5-day | Reacts quickly to price changes |
| Long-term SMA | 15-day | Represents the broader trend |

### Signal Logic

| Condition | Signal |
|-----------|--------|
| Short SMA **crosses above** Long SMA | 🟢 **BUY** — trend turning bullish |
| Short SMA **crosses below** Long SMA | 🔴 **SELL** — trend turning bearish |

The strategy assumes you go **100% in on buy** and **100% out on sell** (no partial position sizing).

---

## 🖥️ What the Dashboard Shows

1. **Metrics row** — Total buy signals, sell signals, strategy return %, and buy-&-hold return % for comparison
2. **Interactive chart** — Closing price, both SMA lines, and green ▲ / red ▼ markers for each trade
3. **Trade Log** — A table of every buy/sell action with date and price
4. **Raw Data** — Expandable view of the underlying data with SMA values

---

## 🎛️ Parameters (Sidebar)

| Parameter | What it does |
|-----------|-------------|
| **Stock Symbol** | The ticker to analyze (e.g. `RELIANCE.NS`, `AAPL`) |
| **Start Date** | Beginning of the historical period |
| **End Date** | End of the historical period |
| **Short-term SMA** | Window (days) for the fast-moving average |
| **Long-term SMA** | Window (days) for the slow-moving average |

### Symbol Format Guide

| Market | Format | Example |
|--------|--------|---------|
| NSE India | `SYMBOL.NS` | `RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `HDFCBANK.NS` |
| BSE India | `SYMBOL.BO` | `RELIANCE.BO` |
| US Market | Plain ticker | `AAPL`, `TSLA`, `MSFT`, `GOOGL` |

---

## 🛠️ Tech Stack

| Library | Role |
|---------|------|
| `streamlit` | Web UI framework |
| `yfinance` | Fetches historical stock data from Yahoo Finance |
| `pandas` | Data manipulation and signal computation |
| `numpy` | Vectorized calculations |
| `matplotlib` | Chart rendering |

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/backtesting.git
cd backtesting
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
backtesting/
├── app.py              # Main Streamlit application
├── BACKTEST.ipynb      # Jupyter notebook (exploratory analysis)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚠️ Limitations & Disclaimers

- This is a **simplified model** — it ignores brokerage fees, taxes, slippage, and liquidity
- SMA crossover is a **lagging indicator** — signals come after the trend has already started
- **Past performance does not guarantee future results**
- This tool is for **educational purposes only**, not financial advice

---

## 💡 Possible Improvements

- [ ] Add RSI, MACD, or Bollinger Bands strategies
- [ ] Add position sizing (e.g., invest fixed ₹ amount per trade)
- [ ] Add stop-loss / take-profit logic
- [ ] Add Sharpe Ratio and max drawdown metrics
- [ ] Portfolio-level backtesting across multiple stocks
