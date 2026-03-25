import pandas as pd
from fredapi import Fred
import os

FRED_API_KEY = os.getenv("FRED_API_KEY") or "b1027bcca0dac4dc6f2fce28ad9178b0"

fred = Fred(api_key=FRED_API_KEY)

SERIES = {
    "hy_spread": "BAMLH0A0HYM2", #us high yield spread
    "loan_spread": "BAMLH0A3HYC", #us leveraged loan spread
    "fed_funds": "FEDFUNDS" #us federal funds rate
}

def fetch_fred_data():
    df = pd.DataFrame()
    for name, code in SERIES.items():
        df[name] = fred.get_series(code)
    df.index.name = "date"
    df = df.dropna()
    df.to_csv("data/processed/fred_data.csv")
    return df