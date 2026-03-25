import yfinance as yf
import pandas as pd

TICKERS = ["ARCC", "OBDC"]

def fetch_bdc_data():
    data = {}
    for t in TICKERS:
        ticker = yf.Ticker(t)
        hist = ticker.history(period="5y", interval="1d")
        data[t] = hist["Close"]
    df = pd.DataFrame(data)
    df["avg_bdc"] = df.mean(axis=1)
    df.to_csv("data/processed/bdc_prices.csv")
    return df