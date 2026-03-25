import plotly.graph_objects as go
import plotly.io as pio

def apply_nyt_moma_theme():
    """
    Registers and applies a custom Plotly template that embodies
    a "NYT meets MoMA" aesthetic: minimalist, high contrast, elegant typography.
    """
    
    # Define colors
    bg_color = "rgba(252, 252, 250, 1)" # Very subtle off-white paper texture feel
    text_color = "#111111" # Near black
    grid_color = "#E5E5E5" # Very faint gray for grid lines
    
    moma_palette = [
        "#E63946", # Bold MoMA Red
        "#1D3557", # Deep Navy
        "#457B9D", # Muted Blue
        "#A8DADC", # Light Cyan
        "#000000", # Pure Black
        "#F4A261", # Ochre
        "#2A9D8F", # Teal
    ]

    # Create template
    pio.templates["nyt_moma"] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                color=text_color,
                size=12
            ),
            title=dict(
                font=dict(
                    family="'Lora', 'Georgia', serif",
                    size=22,
                    color=text_color
                ),
                x=0.01,
                xanchor="left",
                yanchor="top",
            ),
            colorway=moma_palette,
            hovermode="x unified",
            xaxis=dict(
                showline=True,
                linewidth=1,
                linecolor=text_color,
                showgrid=False,
                ticks="outside",
                tickfont=dict(size=11, color="#555555"),
                title_font=dict(size=13, color=text_color, family="'Inter', sans-serif"),
                zeroline=False
            ),
            yaxis=dict(
                showline=False,
                showgrid=True,
                gridwidth=1,
                gridcolor=grid_color,
                tickfont=dict(size=11, color="#555555"),
                title_font=dict(size=13, color=text_color, family="'Inter', sans-serif"),
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor="#999999"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11)
            ),
            margin=dict(l=40, r=40, t=80, b=40)
        )
    )
    
    pio.templates.default = "nyt_moma"
