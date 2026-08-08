"""
Reusable Plotly chart builders for the Streamlit frontend.
"""

import plotly.graph_objects as go
import plotly.colors as pc
import pandas as pd


def top_skills_bar_chart(df, category_col="skill_name", value_col="frequency_count"):
    """2D bar chart — dark theme, Viridis gradient, k-formatted value labels."""
    df = df.sort_values(value_col, ascending=False).reset_index(drop=True)

    def fmt_label(v):
        return f"{v/1000:.1f}k" if v >= 1000 else str(int(v))

    labels = df[value_col].apply(fmt_label)

    fig = go.Figure(
        data=go.Bar(
            x=df[category_col],
            y=df[value_col],
            text=labels,
            textposition="outside",
            marker=dict(
                color=df[value_col],
                colorscale="Viridis",
                colorbar=dict(title=value_col),
                line=dict(width=0),
            ),
        )
    )

    fig.update_layout(
        title="🔥 Interactive Top Skills Demand",
        template="plotly_dark",
        xaxis=dict(tickangle=-45, title=""),
        yaxis=dict(title="Frequency Count"),
        margin=dict(t=60, b=100),
        height=550,
        bargap=0.25,
    )
    return fig


def _cuboid(x0, x1, y0, y1, z0, z1, color):
    """Ek bar (cuboid) Mesh3d se — Plotly mein native 3D bar trace nahi hota."""
    return go.Mesh3d(
        x=[x0, x0, x1, x1, x0, x0, x1, x1],
        y=[y0, y1, y1, y0, y0, y1, y1, y0],
        z=[z0, z0, z0, z0, z1, z1, z1, z1],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color,
        opacity=1,
        flatshading=True,
        showscale=False,
        hoverinfo="skip",
    )


def bar3d_chart(df, category_col, value_col, color_col=None, title="", bar_width=0.6, colorscale="Tealgrn"):
    """3D bar chart (optional — agar future mein kahin 3D dikhana ho)."""
    df = df.reset_index(drop=True)
    color_col = color_col or value_col
    vmin, vmax = df[color_col].min(), df[color_col].max()

    def scale_color(v):
        return 0.5 if vmax == vmin else (v - vmin) / (vmax - vmin)

    scale = pc.get_colorscale(colorscale)
    fig = go.Figure()

    for idx, row in df.iterrows():
        x0, x1 = idx, idx + bar_width
        y0, y1 = 0, bar_width
        z0, z1 = 0, row[value_col]
        color = pc.sample_colorscale(scale, [scale_color(row[color_col])])[0]

        fig.add_trace(_cuboid(x0, x1, y0, y1, z0, z1, color))
        fig.add_trace(go.Scatter3d(
            x=[(x0 + x1) / 2], y=[(y0 + y1) / 2], z=[z1],
            mode="markers", marker=dict(size=4, color=color),
            text=f"{row[category_col]}<br>{value_col}: {row[value_col]}",
            hoverinfo="text", showlegend=False,
        ))
        fig.add_trace(go.Scatter3d(
            x=[(x0 + x1) / 2], y=[y1 + 0.3], z=[0],
            mode="text", text=[str(row[category_col])],
            textposition="middle center", showlegend=False, hoverinfo="skip",
        ))

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(title=value_col),
            camera=dict(eye=dict(x=1.6, y=1.6, z=0.9)),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=550,
    )
    return fig