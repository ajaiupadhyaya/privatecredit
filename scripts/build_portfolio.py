"""Build a self-contained portfolio from the saved database and validated results.

No network calls. Macro snapshot is excluded because provenance is unverified.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.models.liquidity_stress import liquidity_stress_simulation

TICKERS = ['ARCC', 'FSK', 'MAIN', 'OBDC', 'PSEC']


def basket(prices):
    """Daily-rebalanced equal-weight basket on the common observation window."""
    prices = prices[TICKERS].dropna().sort_index()
    if len(prices) < 2 or (prices <= 0).any().any():
        raise ValueError('At least two common observations with positive prices required')
    if prices.index.duplicated().any(): raise ValueError('Duplicate observation dates')
    returns = prices.pct_change(fill_method=None).iloc[1:].mean(axis=1)
    index = pd.concat([pd.Series([100.0], index=prices.index[:1]), 100 * (1 + returns).cumprod()])
    return index, index / index.cummax() - 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--credit-summary', type=Path, default=ROOT/'data/portfolio/credit_summary.json')
    args = parser.parse_args()
    database = ROOT/'data/db/privatecredit.db'
    with sqlite3.connect(f'file:{database}?mode=ro', uri=True) as conn:
        prices = pd.read_sql('SELECT Date, ARCC, FSK, MAIN, OBDC, PSEC FROM bdc_prices ORDER BY Date', conn, parse_dates=['Date']).set_index('Date')
    index, drawdown = basket(prices)
    monthly = pd.DataFrame({'index':index, 'drawdown':drawdown}).resample('ME').last()
    monthly.index = [min(d, index.index[-1]) for d in monthly.index]
    market = dict(start=str(index.index[0].date()), end=str(index.index[-1].date()), observations=len(index), tickers=TICKERS,
        source='Bundled SQLite snapshot; original fetch timestamps and adjustment settings were not recorded.',
        provenance='Unverified snapshot', database_sha256=hashlib.sha256(database.read_bytes()).hexdigest(),
        methodology='Daily-rebalanced equal-weight basket, common trading dates, rebased to 100. Monthly endpoint display. Maximum drawdown calculated on daily observations. No transaction costs.',
        max_drawdown=float(drawdown.min()), final_index=float(index.iloc[-1]),
        series=[dict(date=str(d.date()), value=round(float(r['index']),4), drawdown=round(float(r.drawdown)*100,4)) for d,r in monthly.iterrows()],
        limitations=['Listed BDC equity prices are a liquid proxy, not direct private loan valuations.',
            'The bundled price history is unverified; returns cannot be claimed as a verified total-return backtest.',
            'Survivorship bias and a fixed five-name basket limit representativeness.',
            'The macro table is excluded: the original loader silently substituted synthetic data.'])
    credit = json.loads(args.credit_summary.read_text())
    payload = dict(title='Credit Observatory', market=market, credit=credit,
                   liquidity=liquidity_stress_simulation(100, .3, .1, .85).to_dict('records'))
    report = (ROOT/'data/portfolio/credit_report.html' if args.credit_summary.resolve() == (ROOT/'data/portfolio/credit_summary.json').resolve() else args.credit_summary.parent/'REPORT.html')
    if credit['source_sha256'] not in report.read_text():
        raise ValueError('Credit report and summary source hashes must match')
    public = ROOT/'frontend/public'
    public.mkdir(parents=True, exist_ok=True)
    (public/'research.json').write_text(json.dumps(payload, indent=2, allow_nan=False)+'\n')
    (public/'data.js').write_text('window.RESEARCH = '+json.dumps(payload, allow_nan=False)+';\n')
    out = ROOT/'dist'
    out.mkdir(exist_ok=True)
    for name in ['index.html', 'app.js', 'domain.js', 'styles.css']:
        if (ROOT/'frontend'/name).exists(): shutil.copy2(ROOT/'frontend'/name, out/name)
    shutil.copy2(report, out/'credit-report.html')
    for name in ['research.json','data.js']: shutil.copy2(public/name, out/name)
    print(f'Built {out}; {len(index)} common-date price observations; {credit["rows"]} synthetic loans')

if __name__ == '__main__': main()
