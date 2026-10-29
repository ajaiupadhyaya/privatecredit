import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import sys
import os
# Ensure root directory is in the path to find 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.db_manager import load_dataframe
from src.viz.theme import apply_nyt_moma_theme
from src.features.quant_metrics import calculate_rolling_volatility, calculate_drawdowns, compute_fragility_index, merton_distance_to_default

# 1. Initialize Configuration & Styling
st.set_page_config(layout="wide", page_title="Private Credit Structure", initial_sidebar_state="collapsed")
apply_nyt_moma_theme()

with open("dashboard/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Full-bleed html header
st.html(r"""
<div style="background-color: #000; color: #FFF; width: 100vw; position: relative; margin-left: -50vw; left: 50%; padding: 6rem 10%; margin-bottom: 3rem;">
    <h5 style="color: #E63946; font-family: 'Inter', sans-serif; letter-spacing: 2px; text-transform: uppercase;">Quantitative Analysis Series</h5>
    <h1 style="font-family: 'Lora', serif; font-size: 4.5rem; color: #FFF; line-height: 1.1; margin-bottom: 1rem; border: none;">The Architecture<br>of Fragility</h1>
    <p style="font-family: 'Inter', sans-serif; font-size: 1.4rem; font-weight: 300; max-width: 800px; color: #AAA;">
    A structural deep dive into private credit exposing the friction between floating rates, 
    yield curve regimes, and the mathematical distance to default.
    </p>
</div>
""")

st.warning("Legacy research view: the bundled macro snapshot has unverified provenance and may be simulated. Do not interpret it as observed market evidence. Use the Credit Observatory portfolio for validated results.")

# 2. Data Loading & Processing
@st.cache_data
def load_and_prep_data():
    bdc_prices = load_dataframe("bdc_prices", index_col="Date", parse_dates=["Date"])
    bdc_returns = load_dataframe("bdc_returns", index_col="Date", parse_dates=["Date"])
    macro = load_dataframe("macro_data", index_col="date", parse_dates=["date"])
    
    merged = pd.merge(bdc_prices[['bdc_index']], macro, left_index=True, right_index=True, how='inner')
    merged['bdc_drawdown'] = calculate_drawdowns(merged['bdc_index'])
    merged['bdc_volatility'] = calculate_rolling_volatility(bdc_returns['bdc_index_return'])
    merged['fragility_index'] = compute_fragility_index(merged['hy_spread'], merged['base_rate'], merged['delinquency_rate'])
    
    # Advanced metrics
    merged['merton_dd'] = merton_distance_to_default(merged['bdc_volatility'], merged['base_rate'])
    
    return merged.dropna()

try:
    df = load_and_prep_data()
except Exception as e:
    st.error("Database missing advanced columns. Run `uv run python src/data/init_data.py`.")
    st.stop()


# --- SECTION 1: MACRO REGIMES (YIELD CURVE & SPREADS) ---
st.markdown("<h2>I. The Macro Regime Shift</h2>", unsafe_allow_html=True)
st.markdown("""
<p>
Before analyzing individual credit structures, we must locate ourselves temporally within the macro credit cycle. 
We map the <b>10Y-2Y Yield Curve Inversion</b> against the <b>BAA Corporate Spread</b>. Yield curve inversions 
typically precede liquidity crunches, and when combined with widening corporate spreads, signal deep systemic friction.
</p>
""", unsafe_allow_html=True)

# 2D Regime Scatter / Heatmap
fig_regime = go.Figure()
# Color by fragility index
fig_regime.add_trace(go.Scatter(
    x=df['t10y2y'],
    y=df['baa10y'],
    mode='markers',
    marker=dict(
        size=8,
        color=df['fragility_index'],
        colorscale='RdBu_r',
        showscale=True,
        colorbar=dict(title=dict(text="Fragility", font=dict(family="Inter", size=12)), thickness=15)
    ),
    text=df.index.strftime('%Y-%m-%d'),
    hovertemplate='<b>Date</b>: %{text}<br><b>Yield Curve (2s10s)</b>: %{x:.2f}%<br><b>BAA Spread</b>: %{y:.2f}%<br><b>Fragility</b>: %{marker.color:.1f}'
))

fig_regime.add_vline(x=0, line_dash="dash", line_color="#111", annotation_text="Inversion Boundary")
fig_regime.add_hline(y=df['baa10y'].mean(), line_dash="dot", line_color="#999")

fig_regime.update_layout(
    title="Yield Curve Inversion vs Corporate Spreads",
    xaxis_title="10Y - 2Y Treasury Yield Spread (%)",
    yaxis_title="BAA Corporate - 10Y Yield Spread (%)",
    height=500
)
st.plotly_chart(fig_regime, width="stretch")

st.html(r"""
<div style="background-color: #F8F9FA; border-top: 2px solid #000; border-bottom: 2px solid #000; padding: 2rem 0; margin: 3rem 0;">
    <div style="display: flex; justify-content: space-around; text-align: center;">
        <div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #777; text-transform: uppercase;">Current Regime</div>
            <div style="font-family: 'Lora', serif; font-size: 2.2rem; font-weight: 700;">
""" + ("Inverted & Stressed" if df['t10y2y'].iloc[-1] < 0 and df['baa10y'].iloc[-1] > df['baa10y'].mean() else ("Accommodative" if df['t10y2y'].iloc[-1] > 0 and df['baa10y'].iloc[-1] < df['baa10y'].mean() else "Transitional")) + r"""
            </div>
        </div>
        <div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #777; text-transform: uppercase;">Merton Distance-to-Default</div>
            <div style="font-family: 'Inter', sans-serif; font-size: 2.2rem; font-weight: 700;">""" + f"{df['merton_dd'].iloc[-1]:.2f}σ" + r"""</div>
        </div>
    </div>
</div>
""")

# --- SECTION 2: MERTON's STRUCTURAL DEFAULT PROXY ---
st.markdown("<h2>II. Structural Risk Pricing (Merton Model)</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("""
    <p>
    We treat the equity of Business Development Companies (BDCs) as a Call Option on their underlying asset portfolios (the loans). 
    Using the <b>Merton Distance-to-Default (DD)</b> framework, we infer systemic distress directly from the volatility of public equity markets and floating risk-free rates.
    </p>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    DD_t = \frac{\ln\left(\frac{V_A}{D}\right) + \left(r - \frac{\sigma_V^2}{2}\right)T}{\sigma_V \sqrt{T}}
    ''')
    
    st.markdown(r"""
    <p style="font-size:0.95rem; color: #555;">
    <i>Where $V_A$ is the implied asset value, $D$ is total debt, $\sigma_V$ is implied asset volatility (proxied here by delevered equity volatility), and $r$ is the risk-free rate. A lower DD indicates higher default risk.</i>
    </p>
    """, unsafe_allow_html=True)

with col2:
    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(x=df.index, y=df['merton_dd'], mode='lines',
                              line=dict(color='#E63946', width=2),
                              name='Distance-to-Default (σ)'))
    fig_dd.update_layout(title="Merton Distance-to-Default Proxy Over Time", 
                         yaxis_title="Standard Deviations to Default",
                         yaxis=dict(autorange="reversed"), # Reversed because lower is worse
                         height=350)
    st.plotly_chart(fig_dd, width="stretch")


# --- SECTION 3: THE 3D CONTAGION SURFACE ---
st.markdown("<h2>III. The 3D Contagion Surface</h2>", unsafe_allow_html=True)
st.markdown("""
<p>
The interplay of time, equity volatility, and High-Yield credit spreads creates a physical "surface" of risk. 
Below, we visualize the temporal evolution. Peaks on this surface indicate moments of extreme mismatch—where 
both public equity panic and tight private credit conditions sync up.
</p>
""", unsafe_allow_html=True)

# Generate a 3D surface mapping Date index, Volatility, and HY Spread.
# Since 3D surfaces require a grid, we'll use a 3D scatter to map the temporal path.
fig3d = go.Figure(data=[go.Scatter3d(
    x=df.index, 
    y=df['bdc_volatility'], 
    z=df['hy_spread'],
    mode='lines+markers',
    marker=dict(
        size=4,
        color=df['fragility_index'],
        colorscale='Inferno',
        opacity=0.8
    ),
    line=dict(
        color='#111',
        width=2
    )
)])

fig3d.update_layout(
    scene=dict(
        xaxis_title='Time',
        yaxis_title='Equity Volatility (BDC)',
        zaxis_title='HY Spread (%)',
        camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
    ),
    height=600,
    margin=dict(l=0, r=0, b=0, t=0),
    title_text="Temporal Risk Trajectory"
)
st.plotly_chart(fig3d, width="stretch")

st.html(r"""
<div style="margin-top: 4rem; text-align: center; color: #888; font-family: 'Inter', sans-serif; font-size: 0.85rem;">
    Wall Street Analytical Engine • Executed with Precision • 2026
</div>
""")