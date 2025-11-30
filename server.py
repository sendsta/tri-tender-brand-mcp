"""
Tri-Tender Brand & Letterhead MCP
FastMCP-compatible server for FastMCP Cloud.

Responsibilities:
- Read company brand assets (PDF, DOCX, images).
- Detect logos, dominant colors, fonts, and hex colors.
- Build a BrandProfile JSON object.
- Generate HTML letterhead templates and wrapped documents.
- Produce graph style guides and SVG/PNG bar charts.
- Generate a Brand Book (HTML + PDF as base64 data URL).
"""

from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import List, Dict, Any

from fastmcp import FastMCP

from brand_engine.brand_profile import BrandProfile
from brand_engine.extractors import extract_brand_from_files
from brand_engine.templates import (
    generate_letterhead_template,
    wrap_body_in_letterhead,
    generate_graph_style_guide,
)
from brand_engine.charts import (
    generate_bar_chart_svg,
    generate_bar_chart_png_base64,
)
from brand_engine.brand_book import (
    generate_brand_book_html,
    generate_brand_book_pdf_data_url,
)

mcp = FastMCP(
    name="tri-tender-brand-letterhead-mcp",
    description="Brand & Letterhead Engine for Tri-Tender: builds brand profiles, letterheads, charts, and brand books.",
)


@mcp.tool()
async def build_brand_profile(file_paths: List[str]) -> Dict[str, Any]:
    """
    Analyze the given brand assets and return a BrandProfile.

    Args:
        file_paths: List of paths to PDFs, DOCX, images or brand-guide files
                    accessible to this MCP server (e.g. via FastMCP Cloud).

    Returns:
        Dict representing the BrandProfile.
    """
    profile: BrandProfile = extract_brand_from_files(file_paths)
    return asdict(profile)


@mcp.tool()
async def get_letterhead_template(brand_profile: Dict[str, Any]) -> str:
    """
    Generate an HTML letterhead template using BrandProfile CSS tokens.

    Args:
        brand_profile: A BrandProfile dict (e.g. from build_brand_profile).

    Returns:
        HTML string containing a styled letterhead template.
    """
    profile = BrandProfile.from_dict(brand_profile)
    return generate_letterhead_template(profile)


@mcp.tool()
async def render_letter_with_body(
    brand_profile: Dict[str, Any],
    body_html: str,
    title: str = "Tri-Tender Document",
) -> str:
    """
    Wrap arbitrary body HTML into the brand letterhead.

    Args:
        brand_profile: BrandProfile dict.
        body_html: Inner HTML of the document body.
        title: <title> tag for the HTML page.

    Returns:
        Full HTML document as a string.
    """
    profile = BrandProfile.from_dict(brand_profile)
    return wrap_body_in_letterhead(profile, body_html, title=title)


@mcp.tool()
async def get_graph_style(brand_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a graph style guide for charts (series colors, fonts, etc.).

    Args:
        brand_profile: BrandProfile dict.

    Returns:
        Graph style guide as dict.
    """
    profile = BrandProfile.from_dict(brand_profile)
    return generate_graph_style_guide(profile)


@mcp.tool()
async def build_bar_chart_svg(
    brand_profile: Dict[str, Any],
    series: List[Dict[str, Any]],
    title: str = "",
    width: int = 800,
    height: int = 400,
) -> str:
    """
    Generate an inline SVG bar chart using the brand chart palette.

    Args:
        brand_profile: BrandProfile dict.
        series: List of { "label": str, "value": float }.
        title: Optional chart title.
        width: Width of SVG.
        height: Height of SVG.

    Returns:
        SVG XML string.
    """
    profile = BrandProfile.from_dict(brand_profile)
    return generate_bar_chart_svg(profile, series, title=title, width=width, height=height)


@mcp.tool()
async def build_bar_chart_png(
    brand_profile: Dict[str, Any],
    series: List[Dict[str, Any]],
    title: str = "",
    width: int = 800,
    height: int = 400,
) -> str:
    """
    Generate a PNG bar chart as a base64 data URL using brand palette.

    Args:
        brand_profile: BrandProfile dict.
        series: List of { "label": str, "value": float }.
        title: Optional chart title.
        width: Width of PNG.
        height: Height of PNG.

    Returns:
        A data URL string: "data:image/png;base64,...."
    """
    profile = BrandProfile.from_dict(brand_profile)
    return generate_bar_chart_png_base64(profile, series, title=title, width=width, height=height)


@mcp.tool()
async def generate_brand_book(brand_profile: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate a Brand Book summarizing all brand elements inferred for the client.

    Returns a dict with:
      - html: HTML string for the Brand Book (multi-section document).
      - pdf_data_url: base64 data URL for a PDF version (data:application/pdf;base64,...).

    This is ideal to store in Tri-Tender's project space as a brand reference,
    and to share with the client as a polished brand kit.
    """
    profile = BrandProfile.from_dict(brand_profile)
    html = generate_brand_book_html(profile)
    pdf_data_url = generate_brand_book_pdf_data_url(profile, html)
    return {
        "html": html,
        "pdf_data_url": pdf_data_url,
    }


if __name__ == "__main__":
    mcp.run()
