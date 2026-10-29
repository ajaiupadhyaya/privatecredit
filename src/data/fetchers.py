import os
import yfinance as yf
import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta
import numpy as np

# Try to get FRED API key from environment
FRED_API_KEY = os.environ.get("FRED_API_KEY")

def fetch_bdc_data(start_date="2018-01-01"):
    """
    Fetches historical data for major Business Development Companies (BDCs)
    as proxies for Private Credit performance.
    """
    bdc_tickers = ["ARCC", "OBDC", "FSK", "MAIN", "PSEC"]
    try:
        data = yf.download(bdc_tickers, start=start_date, end=datetime.today().strftime('%Y-%m-%d'))
        
        if "Adj Close" in data:
            prices = data["Adj Close"]
        else:
            prices = data["Close"]
            
        prices.dropna(how='all', inplace=True)
        # Forward fill missing values (like weekends or holidays for specific stocks)
        prices.ffill(inplace=True)
        
        # Calculate daily returns
        returns = prices.pct_change().dropna()
        
        # Calculate a simple equal-weighted BDC index
        returns['bdc_index_return'] = returns.mean(axis=1)
        prices['bdc_index'] = (1 + returns['bdc_index_return']).cumprod() * 100
        
        return prices, returns
    except Exception as e:
        print(f"Error fetching BDC data from yfinance: {e}")
        return pd.DataFrame(), pd.DataFrame()

def fetch_macro_data(start_date="2018-01-01", allow_synthetic=False):
    """
    Fetches macroeconomic indicators from FRED:
    - BAMLH0A0HYM2: ICE BofA US High Yield Index Option-Adjusted Spread
    - SOFR: Secured Overnight Financing Rate (or EFFR if older)
    - DRBLACBS: Delinquency Rate on Business Loans
    """
    if not FRED_API_KEY:
        if allow_synthetic:
            return _generate_mock_macro(start_date)
        raise RuntimeError("FRED_API_KEY is required. Synthetic data must be explicitly requested.")
        
    try:
        fred = Fred(api_key=FRED_API_KEY)
        
        # Fetch series
        hy_spread = fred.get_series('BAMLH0A0HYM2', observation_start=start_date)
        sofr = fred.get_series('SOFR', observation_start=start_date)
        # If SOFR is missing early data, we might need EFFR
        if sofr.empty or sofr.index[0] > pd.to_datetime('2019-01-01'):
            effr = fred.get_series('EFFR', observation_start=start_date)
            # Combine EFFR and SOFR
            rates = pd.concat([effr, sofr], axis=1)
            rates.columns = ['EFFR', 'SOFR']
            combined_rate = rates['SOFR'].fillna(rates['EFFR'])
        else:
            combined_rate = sofr
            
        try:
            delinquency = fred.get_series('DRBLACBS', observation_start=start_date)
        except:
            delinquency = pd.Series(dtype=float)
            
        try:
            t10y2y = fred.get_series('T10Y2Y', observation_start=start_date)
            baa10y = fred.get_series('BAA10Y', observation_start=start_date)
        except:
            t10y2y = pd.Series(dtype=float)
            baa10y = pd.Series(dtype=float)
        
        # Resample delinquency (quarterly) to daily by forward filling
        df = pd.DataFrame({
            'hy_spread': hy_spread,
            'base_rate': combined_rate,
            't10y2y': t10y2y,
            'baa10y': baa10y
        })
        
        # Add delinquency with daily frequency
        delinq_df = pd.DataFrame({'delinquency_rate': delinquency})
        df = df.join(delinq_df, how='outer')
        df['delinquency_rate'] = df['delinquency_rate'].ffill()
        df['t10y2y'] = df['t10y2y'].ffill()
        df['baa10y'] = df['baa10y'].ffill()
        
        df.dropna(subset=['hy_spread'], inplace=True)
        df.ffill(inplace=True)
        return df

    except Exception as e:
        print(f"Error fetching FRED data: {e}")
        if allow_synthetic:
            return _generate_mock_macro(start_date)
        raise RuntimeError("FRED retrieval failed; no synthetic substitution was made") from e

def _generate_mock_macro(start_date="2018-01-01"):
    """Generates synthetic macro data if FRED API is unavailable."""
    dates = pd.date_range(start=start_date, end=datetime.today(), freq='B')
    n = len(dates)
    
    # Simulate a rate hike cycle
    t = np.linspace(0, 10, n)
    base_rate = 1.5 + np.sin(t*0.5)*1.5 + (t > 7)*3 # Spike after some time
    
    # Spreads widen when rates spike and stay high
    spreads = 3.5 + np.random.normal(0, 0.2, n) + (t > 7)*2 + np.sin(t*2)*0.5
    
    # Delinquency follows with a lag
    delinq = 1.2 + (t > 8)*1.5 + np.random.normal(0, 0.1, n)
    
    # Yield curve T10Y2Y (inverts during rate spikes)
    t10y2y = 1.0 - (t > 5)*1.5 + np.random.normal(0, 0.1, n)
    
    # BAA Corporate vs 10Y
    baa10y = 2.0 + (t > 7)*1.5 + np.random.normal(0, 0.1, n)
    
    df = pd.DataFrame({
        'hy_spread': np.maximum(spreads, 2.0),
        'base_rate': np.maximum(base_rate, 0.0),
        'delinquency_rate': np.maximum(delinq, 0.5),
        't10y2y': t10y2y,
        'baa10y': np.maximum(baa10y, 0.5)
    }, index=dates)
    
    df.index.name = "date"
    return df
