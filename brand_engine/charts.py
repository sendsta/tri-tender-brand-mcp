from __future__ import annotations

import io
from typing import List, Dict, Any

import matplotlib.pyplot as plt

from .brand_profile import BrandProfile


def generate_bar_chart_svg(
    profile: BrandProfile,
    series: List[Dict[str, Any]],
    title: str = "",
    width: int = 800,
    height: int = 400,
) -> str:
    """
    Generate a simple vertical bar chart as inline SVG using matplotlib.
    """
    profile.ensure_palette()

    labels = [str(s.get("label", "")) for s in series]
    values = [float(s.get("value", 0.0)) for s in series]

    fig_w = width / 96.0  # dpi -> inches
    fig_h = height / 96.0

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    colors = profile.chart_palette or ["#2563EB"]

    bars = ax.bar(labels, values)

    # Apply brand colors per bar
    for i, bar in enumerate(bars):
        bar.set_color(colors[i % len(colors)])

    if title:
        ax.set_title(title, fontfamily=profile.font_heading.split(",")[0].strip("'\""))

    ax.set_ylabel("")
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.4)

    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight")
    plt.close(fig)
    svg = buf.getvalue()
    buf.close()
    return svg


def generate_bar_chart_png_base64(
    profile: BrandProfile,
    series: List[Dict[str, Any]],
    title: str = "",
    width: int = 800,
    height: int = 400,
) -> str:
    """
    Generate a bar chart as PNG (base64 data URL).
    """
    import base64

    profile.ensure_palette()

    labels = [str(s.get("label", "")) for s in series]
    values = [float(s.get("value", 0.0)) for s in series]

    fig_w = width / 96.0
    fig_h = height / 96.0

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    colors = profile.chart_palette or ["#2563EB"]

    bars = ax.bar(labels, values)
    for i, bar in enumerate(bars):
        bar.set_color(colors[i % len(colors)])

    if title:
        ax.set_title(title, fontfamily=profile.font_heading.split(",")[0].strip("'\""))

    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.4)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    png_bytes = buf.getvalue()
    buf.close()

    encoded = base64.b64encode(png_bytes).decode("ascii")
    return f"data:image/png;base64,{encoded}"
