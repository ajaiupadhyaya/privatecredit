import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide", page_title="Private Credit Fragility Dashboard")

st.title("Private Credit Fragility: Hidden Risk Analysis")

# Fragility Index
fragility = pd.read_csv("data/processed/fragility_index.csv", index_col="date", parse_dates=True)
fig1 = px.line(fragility, y=["fragility_index", "fragility_index_smooth"], title="Private Credit Fragility Index")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
**Insight:** Fragility index highlights hidden risk not captured by NAV or market prices alone.
""")

# NAV vs HY Spread
st.subheader("BDC NAV vs High Yield Spread")
nav_hy = pd.read_csv("data/processed/bdc_prices.csv", index_col="Date", parse_dates=True).join(
    pd.read_csv("data/processed/fred_data.csv", index_col="date", parse_dates=True), how="inner"
)
fig2 = px.line(nav_hy, y=["avg_bdc", "hy_spread"], title="BDC NAV vs HY Spread")
st.plotly_chart(fig2, use_container_width=True)

# Liquidity Stress Simulation
st.subheader("Liquidity Stress Simulation")
liq = pd.read_csv("data/processed/liquidity_sim.csv")
fig3 = px.line(liq, x="period", y="remaining_assets", title="Liquidity Stress Test")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
**Insight:** Even moderate redemption shocks cause significant NAV erosion due to illiquid assets.
""")

# GIF / Animated Visual Example (optional)
st.subheader("Interactive Fragility Over Time")
st.markdown("This animation shows fragility index evolution and macro conditions.")
# Example: generate animated chart using Plotly Express with frames
fig_anim = px.line(fragility, x=fragility.index, y="fragility_index", title="Fragility Index Animation")
st.plotly_chart(fig_anim)