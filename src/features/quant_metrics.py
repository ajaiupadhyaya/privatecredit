import pandas as pd
import numpy as np
from scipy import stats

def calculate_rolling_volatility(returns: pd.Series, window: int = 60, trading_days: int = 252) -> pd.Series:
    """Calculates annualized rolling volatility."""
    return returns.rolling(window=window).apply(lambda x: np.std(x, ddof=1) * np.sqrt(trading_days), raw=False)

def calculate_drawdowns(prices: pd.Series) -> pd.Series:
    """Calculates peak-to-trough drawdowns."""
    rolling_max = prices.cummax()
    drawdowns = (prices - rolling_max) / rolling_max
    return drawdowns

def historical_var(returns: pd.Series, confidence_level: float = 0.95) -> float:
    """Calculates historical Value at Risk (VaR)."""
    return np.percentile(returns, (1 - confidence_level) * 100)

def compute_fragility_index(hy_spread: pd.Series, base_rate: pd.Series, delinq: pd.Series) -> pd.Series:
    r"""
    Computes a synthetic macroscopic fragility index:
    Fragility = \alpha (HY Spread) + \beta (\Delta Base Rate) + \gamma (Delinquency)
    Normalized to start at 100.
    """
    
    # Normalize inputs to Z-scores over a rolling window to remove scale dependency
    window = 252
    z_spread = (hy_spread - hy_spread.rolling(window).mean()) / hy_spread.rolling(window).std()
    
    # We care about rate *hikes*, so we look at momentum
    rate_mom = base_rate.diff(21).rolling(window).mean()
    z_rate = (rate_mom - rate_mom.rolling(window).mean()) / rate_mom.rolling(window).std()
    
    z_delinq = (delinq - delinq.rolling(window).mean()) / delinq.rolling(window).std()
    
    # Weights: Stress on borrowers is driven heavily by borrowing costs
    # Delinquency is a lagging indicator but confirms stress.
    alpha, beta, gamma = 0.4, 0.4, 0.2
    
    raw_fragility = (alpha * z_spread) + (beta * z_rate) + (gamma * z_delinq)
    
    fragility_ewma = raw_fragility.ewm(span=60, adjust=False).mean()
    fragility_index = 100 + (fragility_ewma * 15)
    return fragility_index

def merton_distance_to_default(equity_volatility: pd.Series, risk_free_rate: pd.Series, leverage_ratio: float = 1.0) -> pd.Series:
    r"""
    Approximates Merton's Distance-to-Default (DD) for financials.
    Treats equity as a call option on the asset value of the firm.
    
    Simplified structural proxy:
    Assume D = E * leverage_ratio => V = E(1 + L)
    \sigma_V \approx \sigma_E \times (E/V) = \sigma_E / (1+L)
    
    DD = [\ln(V/D) + (r - \sigma_V^2 / 2)T] / (\sigma_V \sqrt{T})
    Assuming T = 1 year.
    """
    # Normalize risk-free rate to decimal
    r = risk_free_rate / 100.0
    
    # Asset volatility approximation
    sigma_V = equity_volatility / (1.0 + leverage_ratio)
    
    # Ratio V/D = (E+D)/D = (1+L)/L
    v_d_ratio = (1.0 + leverage_ratio) / leverage_ratio
    
    term1 = np.log(v_d_ratio)
    term2 = r - ((sigma_V ** 2) / 2.0)
    
    dd = (term1 + term2) / sigma_V
    return dd
