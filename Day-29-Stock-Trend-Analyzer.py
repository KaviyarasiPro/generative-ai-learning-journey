"""
Day 29: Stock Trend Analyzer
Moving Averages, RSI, Golden/Death Cross signals, Stock comparison

EDUCATIONAL PURPOSE ONLY. This is NOT investment advice and does NOT
predict future prices. It only describes past trends.

Data: real data from Yahoo Finance via yfinance. If there is no internet
(or yfinance fails), the script automatically uses SAMPLE (synthetic) data
so the code still runs.

Install:  pip install yfinance pandas numpy matplotlib
Run:      python Day-29-Stock-Trend-Analyzer.py
Charts are saved in the 'charts' folder.
"""

import os
import re
import zlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # yfinance not installed, fallback data will be used
    yf = None

os.makedirs("charts", exist_ok=True)

DEFAULT_STOCKS = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]
DISCLAIMER = "Educational purpose only. Not investment advice."

# ===============================================================
# PART 1: Data + Indicators + Signals
# ===============================================================


def sample_data(symbol, days=500):
    """Synthetic random-walk prices (used only when real data is unavailable)."""
    rng = np.random.default_rng(zlib.crc32(symbol.encode()))
    returns = rng.normal(0.0004, 0.015, days)
    start = rng.integers(500, 3500)
    close = start * np.exp(np.cumsum(returns))
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=days)
    return pd.DataFrame({"Close": close}, index=dates)


def load_data(symbol, period="2y"):
    """Returns (dataframe, is_real_data)."""
    if yf is not None:
        try:
            df = yf.download(symbol, period=period, progress=False, auto_adjust=True)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            if df is not None and not df.empty and "Close" in df.columns:
                return df[["Close"]].dropna(), True
        except Exception:
            pass
    return sample_data(symbol), False


def add_indicators(df):
    df = df.copy()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["Return"] = df["Close"].pct_change()

    # RSI (14-day, Wilder's smoothing)
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Golden Cross: MA20 crosses ABOVE MA50 | Death Cross: crosses BELOW
    valid = df["MA50"].notna()
    above = (df["MA20"] > df["MA50"]).astype(int).where(valid)
    cross = above.diff()
    df["Golden"] = cross == 1
    df["Death"] = cross == -1
    return df


def trend_summary(df):
    last = df.iloc[-1]
    score = 0
    score += 1 if last["Close"] > last["MA50"] else -1
    score += 1 if last["MA20"] > last["MA50"] else -1

    if score == 2:
        trend = "BULLISH 📈"
    elif score == -2:
        trend = "BEARISH 📉"
    else:
        trend = "NEUTRAL ➖"

    if last["RSI"] > 70:
        rsi_note = "Overbought zone (RSI > 70)"
    elif last["RSI"] < 30:
        rsi_note = "Oversold zone (RSI < 30)"
    else:
        rsi_note = "Normal range (RSI 30-70)"
    return trend, rsi_note


def plot_price_chart(df, symbol, is_real):
    tag = "" if is_real else " (SAMPLE DATA)"
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )
    ax1.plot(df.index, df["Close"], label="Close", color="#3b82f6", linewidth=1.5)
    ax1.plot(df.index, df["MA20"], label="MA20", color="#f59e0b")
    ax1.plot(df.index, df["MA50"], label="MA50", color="#8b5cf6")
    ax1.scatter(df.index[df["Golden"]], df["Close"][df["Golden"]], marker="^",
                color="green", s=110, label="Golden Cross", zorder=5)
    ax1.scatter(df.index[df["Death"]], df["Close"][df["Death"]], marker="v",
                color="red", s=110, label="Death Cross", zorder=5)
    ax1.set_title(f"{symbol} Price with Moving Averages{tag}")
    ax1.set_ylabel("Price")
    ax1.legend(loc="upper left")
    ax1.grid(alpha=0.3)

    ax2.plot(df.index, df["RSI"], color="#10b981")
    ax2.axhline(70, color="red", linestyle="--", linewidth=1)
    ax2.axhline(30, color="green", linestyle="--", linewidth=1)
    ax2.set_ylabel("RSI")
    ax2.set_ylim(0, 100)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    name = re.sub(r"[^A-Za-z0-9]", "_", symbol)
    path = f"charts/{name}_trend.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def analyze(symbol):
    raw, is_real = load_data(symbol)
    df = add_indicators(raw)
    trend, rsi_note = trend_summary(df)
    path = plot_price_chart(df, symbol, is_real)

    last = df.iloc[-1]
    print(f"\n{'=' * 55}")
    print(f"{symbol}  ({'real data' if is_real else 'SAMPLE data, no internet'})")
    print("=" * 55)
    print(f"Last close   : {last['Close']:.2f}")
    print(f"MA20 / MA50  : {last['MA20']:.2f} / {last['MA50']:.2f}")
    print(f"RSI (14)     : {last['RSI']:.1f}  -> {rsi_note}")
    print(f"Trend        : {trend}")
    print(f"Golden Cross : {int(df['Golden'].sum())} time(s) | "
          f"Death Cross: {int(df['Death'].sum())} time(s)")
    print(f"Chart saved  : {path}")
    return df, is_real


# ===============================================================
# PART 2: Compare Stocks + Interactive App
# ===============================================================


def compare_stocks(symbols):
    rows, series = [], {}
    any_sample = False
    for sym in symbols:
        raw, is_real = load_data(sym)
        any_sample = any_sample or not is_real
        close = raw["Close"]
        total_return = (close.iloc[-1] / close.iloc[0] - 1) * 100
        volatility = close.pct_change().std() * np.sqrt(252) * 100
        rows.append({
            "Stock": sym,
            "Return %": round(total_return, 1),
            "Volatility %": round(volatility, 1),
            "Return/Risk": round(total_return / volatility, 2),
        })
        series[sym] = close / close.iloc[0] * 100  # normalised to 100

    table = pd.DataFrame(rows).set_index("Stock")
    print("\n" + "=" * 55)
    print("STOCK COMPARISON (last 2 years)" + ("  [SAMPLE DATA]" if any_sample else ""))
    print("=" * 55)
    print(table)
    print(f"\nHighest return : {table['Return %'].idxmax()}")
    print(f"Most volatile  : {table['Volatility %'].idxmax()}")

    fig, ax = plt.subplots(figsize=(10, 5))
    for sym, s in series.items():
        ax.plot(s.index, s.values, label=sym)
    ax.axhline(100, color="gray", linestyle="--", linewidth=1)
    ax.set_ylabel("Growth (start = 100)")
    ax.set_title("Stock Comparison" + (" (SAMPLE DATA)" if any_sample else ""))
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("charts/stock_comparison.png", dpi=150)
    plt.close()
    print("Chart saved  : charts/stock_comparison.png")


def main():
    print(f"\n⚠️  {DISCLAIMER}")
    analyze(DEFAULT_STOCKS[0])
    compare_stocks(DEFAULT_STOCKS)

    print("\n" + "=" * 55)
    print("   STOCK TREND ANALYZER (type 'exit' to quit)")
    print("=" * 55)
    print("Examples: TCS.NS, INFY.NS, HDFCBANK.NS, AAPL")
    while True:
        symbol = input("\nEnter stock symbol: ").strip().upper()
        if symbol == "EXIT":
            print(f"Thanks! Remember: {DISCLAIMER}")
            break
        if not symbol:
            continue
        analyze(symbol)


if __name__ == "__main__":
    main()