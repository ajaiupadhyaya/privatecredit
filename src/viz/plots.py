import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

sns.set(style="whitegrid")

def plot_fragility_index(file="data/processed/fragility_index.csv"):
    df = pd.read_csv(file, index_col="date", parse_dates=True)
    fig = px.line(df, y=["fragility_index", "fragility_index_smooth"], title="Private Credit Fragility Index")
    fig.write_html("dashboard/fragility_index.html")
    return fig

def plot_hidden_defaults():
    bdc = pd.read_csv("data/processed/bdc_prices.csv", index_col="Date", parse_dates=True)
    fred = pd.read_csv("data/processed/fred_data.csv", index_col="date", parse_dates=True)
    df = bdc.join(fred, how="inner")
    fig = px.line(df, y=["avg_bdc", "hy_spread"], title="BDC NAV vs HY Spread")
    fig.write_html("dashboard/nav_vs_spread.html")
    return fig

def plot_liquidity_stress(file="data/processed/liquidity_sim.csv"):
    df = pd.read_csv(file)
    fig = px.line(df, x="period", y="remaining_assets", title="Liquidity Stress Simulation")
    fig.write_html("dashboard/liquidity_stress.html")
    return fig