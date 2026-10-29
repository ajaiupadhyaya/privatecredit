import pandas as pd
import pytest
from scripts.build_portfolio import basket, TICKERS


def test_equal_weight_returns_not_average_nominal_prices():
    df = pd.DataFrame({t:[10*(i+1),20*(i+1),10*(i+1)] for i,t in enumerate(TICKERS)}, index=pd.date_range('2020-01-01', periods=3))
    index, dd = basket(df)
    assert index.tolist() == pytest.approx([100,200,100])
    assert dd.tolist() == pytest.approx([0,0,-.5])


def test_common_window_excludes_missing_constituents():
    df = pd.DataFrame({t:[10.,11.,12.] for t in TICKERS}, index=pd.date_range('2020-01-01', periods=3))
    df.iloc[0,0] = float('nan')
    index, _ = basket(df)
    assert len(index) == 2
    assert index.iloc[0] == 100
