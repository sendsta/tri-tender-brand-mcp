from __future__ import annotations

import base64
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Flowable,
)

from .brand_profile import BrandProfile


def generate_brand_book_html(profile: BrandProfile) -> str:
    """
    Build a single-page (or multi-section) Brand Book as HTML summarising
    all brand elements inferred for the client.
    """
    profile.ensure_palette()

    name = profile.name or "Your Company Name"
    today = datetime.utcnow().strftime("%Y-%m-%d")

    logo_html = ""
    if profile.logo_path:
        logo_html = f'<img src="{profile.logo_path}" alt="Logo" style="max-height:80px;max-width:260px;object-fit:contain;border-radius:10px;background:#F9FAFB;padding:8px 14px;margin-bottom:16px;" />'

    color_swatches = ""
    for c in profile.chart_palette:
        color_swatches += f"""
        <div class="swatch">
          <div class="swatch-color" style="background:{c};"></div>
          <div class="swatch-label">{c}</div>
        </div>
        """

    fonts_html = ""
    if profile.detected_fonts:
        fonts_html = "<ul>" + "".join(
            f"<li>{f}</li>" for f in profile.detected_fonts
        ) + "</ul>"
    else:
        fonts_html = "<p>No explicit fonts detected. Using default system stack.</p>"

    hex_html = ""
    if profile.hex_colors_in_text:
        hex_html = "<ul>" + "".join(
            f"<li>{h}</li>" for h in profile.hex_colors_in_text
        ) + "</ul>"
    else:
        hex_html = "<p>No inline hex colors detected in brand guides.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{name} – Tri-Tender Brand Book</title>
  <style>
    :root {{
      --brand-primary: {profile.primary_color or "#0B1120"};
      --brand-secondary: {profile.secondary_color or "#2563EB"};
      --brand-accent: {profile.accent_color or "#0EA5E9"};
      --brand-bg: {profile.background_color or "#F9FAFB"};
      --brand-neutral: {profile.neutral_color or "#111827"};
      --font-heading: {profile.font_heading};
      --font-body: {profile.font_body};
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      padding: 0;
      font-family: var(--font-body);
      background: var(--brand-bg);
      color: var(--brand-neutral);
    }}
    .page {{
      max-width: 1024px;
      margin: 24px auto;
      background: #FFFFFF;
      border-radius: 16px;
      box-shadow: 0 18px 50px rgba(15,23,42,0.14);
      overflow: hidden;
    }}
    .cover {{
      padding: 32px 40px 24px 40px;
      background: radial-gradient(circle at top left, var(--brand-secondary), var(--brand-primary));
      color: white;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(15,23,42,0.35);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 8px;
    }}
    .cover h1 {{
      font-family: var(--font-heading);
      font-size: 28px;
      margin: 0 0 4px 0;
    }}
    .cover h2 {{
      font-size: 14px;
      font-weight: 400;
      opacity: 0.9;
      margin: 0 0 16px 0;
    }}
    .meta {{
      font-size: 11px;
      opacity: 0.85;
    }}
    .body {{
      padding: 28px 40px 32px 40px;
      font-size: 14px;
      line-height: 1.6;
    }}
    h3 {{
      font-family: var(--font-heading);
      font-size: 18px;
      margin-top: 0;
      color: var(--brand-primary);
    }}
    h4 {{
      font-family: var(--font-heading);
      font-size: 15px;
      margin-bottom: 6px;
      color: var(--brand-primary);
    }}
    .section {{
      margin-bottom: 24px;
      border-bottom: 1px solid #E5E7EB;
      padding-bottom: 20px;
    }}
    .section:last-child {{
      border-bottom: none;
      padding-bottom: 0;
    }}
    .color-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .swatch {{
      width: 120px;
      background: #F3F4F6;
      border-radius: 12px;
      padding: 10px;
      font-size: 11px;
    }}
    .swatch-color {{
      height: 38px;
      border-radius: 9px;
      margin-bottom: 6px;
      border: 1px solid rgba(15,23,42,0.07);
    }}
    .swatch-label {{
      font-family: var(--font-heading);
      color: #111827;
    }}
    .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 12px;
      padding: 6px 8px;
      background: #F9FAFB;
      border-radius: 8px;
      border: 1px dashed #E5E7EB;
      display: inline-block;
    }}
    .two-column {{
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
      gap: 20px;
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="cover">
      <div class="badge">Tri-Tender • Brand Profile</div>
      <h1>{name}</h1>
      <h2>Generated Brand Book – automated by Tri-Tender Brand Engine</h2>
      <div class="meta">Generated on {today}</div>
      <div style="margin-top:16px;">
        {logo_html}
      </div>
    </section>
    <section class="body">
      <div class="section">
        <h3>1. Overview</h3>
        <p>
          This Brand Book has been generated by the Tri-Tender Brand &amp; Letterhead Engine.
          It summarises all brand elements inferred from your supplied letterheads,
          company profiles, brand guides and logos. These settings are used to
          style tender responses, cover letters, executive summaries and pricing
          schedules generated inside Tri-Tender.
        </p>
      </div>

      <div class="section">
        <h3>2. Core Brand Colors</h3>
        <div class="two-column">
          <div>
            <p>Primary color: <span class="mono">{profile.primary_color or "N/A"}</span></p>
            <p>Secondary color: <span class="mono">{profile.secondary_color or "N/A"}</span></p>
            <p>Accent color: <span class="mono">{profile.accent_color or "N/A"}</span></p>
            <p>Background color: <span class="mono">{profile.background_color}</span></p>
            <p>Neutral text color: <span class="mono">{profile.neutral_color}</span></p>
          </div>
          <div class="color-row">
            {color_swatches}
          </div>
        </div>
      </div>

      <div class="section">
        <h3>3. Typography</h3>
        <p><strong>Heading font-family:</strong></p>
        <p class="mono">{profile.font_heading}</p>
        <p style="margin-top:10px;"><strong>Body font-family:</strong></p>
        <p class="mono">{profile.font_body}</p>
        <h4 style="margin-top:16px;">Detected fonts from PDFs</h4>
        {fonts_html}
      </div>

      <div class="section">
        <h3>4. Logo &amp; Imagery</h3>
        <p>
          The Brand Engine attempts to detect your logo from embedded images inside
          PDF letterheads and other assets. The following logo path is currently
          associated with this profile:
        </p>
        <p class="mono">{profile.logo_path or "None detected"}</p>
        <p style="margin-top:12px;">
          If this is incorrect, you can upload a more accurate logo file and regenerate
          the Brand Profile.
        </p>
      </div>

      <div class="section">
        <h3>5. Hex Colors Found in Brand Guides</h3>
        <p>
          These hex colors were discovered inside your text-based brand guides
          (PDF / DOCX). They are treated as additional palette hints:
        </p>
        {hex_html}
      </div>

      <div class="section">
        <h3>6. Chart &amp; Data Visualisation Palette</h3>
        <p>
          The following palette is used by Tri-Tender when generating graphs in your
          tender submissions (for example spend charts, risk heatmaps or schedules).
          Bars and series rotate through the palette below.
        </p>
        <div class="color-row">
          {color_swatches}
        </div>
      </div>

      <div class="section">
        <h3>7. Usage in Tri-Tender</h3>
        <p>
          Your BrandProfile is applied consistently to:
        </p>
        <ul>
          <li>Letterheads and cover pages for tender submissions.</li>
          <li>Executive summaries and company profiles generated by Tri-Tender.</li>
          <li>Pricing schedules with branded tables and headers.</li>
          <li>Charts and diagrams included in the response pack.</li>
        </ul>
        <p>
          Whenever you adjust your brand (logo, colors or fonts), you can simply
          re-run the Brand Engine on the updated assets and regenerate this Brand Book.
        </p>
      </div>
    </section>
  </div>
</body>
</html>
"""


def generate_brand_book_pdf_data_url(profile: BrandProfile, html_preview: str | None = None) -> str:
    """
    Generate a concise PDF Brand Book using reportlab and return it as
    a base64 data URL (data:application/pdf;base64,...).

    The layout is simpler than the HTML version but carries the same core data.
    """
    profile.ensure_palette()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="Tri-Tender Brand Book",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Heading1TT", parent=styles["Heading1"], fontSize=18, leading=22))
    styles.add(ParagraphStyle(name="Heading2TT", parent=styles["Heading2"], fontSize=14, leading=18))
    styles.add(ParagraphStyle(name="NormalSmall", parent=styles["Normal"], fontSize=9, leading=11))

    story = []

    # Cover-like heading
    name = profile.name or "Your Company Name"
    today = datetime.utcnow().strftime("%Y-%m-%d")

    story.append(Paragraph(f"{name} – Brand Book", styles["Heading1TT"]))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Generated by Tri-Tender Brand & Letterhead Engine", styles["Normal"]))
    story.append(Paragraph(f"Date: {today}", styles["NormalSmall"]))
    story.append(Spacer(1, 10 * mm))

    # Section: Core Colors
    story.append(Paragraph("1. Core Brand Colors", styles["Heading2TT"]))
    story.append(Spacer(1, 2 * mm))
    color_data = [
        ["Primary", profile.primary_color or "N/A"],
        ["Secondary", profile.secondary_color or "N/A"],
        ["Accent", profile.accent_color or "N/A"],
        ["Background", profile.background_color],
        ["Neutral", profile.neutral_color],
    ]
    color_table = Table(color_data, colWidths=[45 * mm, 80 * mm])
    color_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    story.append(color_table)
    story.append(Spacer(1, 6 * mm))

    # Palette row
    if profile.chart_palette:
        story.append(Paragraph("Palette (used for charts & accents):", styles["Normal"]))
        palette_data = [[c for c in profile.chart_palette]]
        palette_table = Table(palette_data, colWidths=[(170 * mm) / max(1, len(profile.chart_palette))] * len(profile.chart_palette), rowHeights=10 * mm)
        palette_style = [("GRID", (0, 0), (-1, -1), 0.25, colors.white)]
        for idx, c in enumerate(profile.chart_palette):
            try:
                palette_style.append(("BACKGROUND", (idx, 0), (idx, 0), colors.HexColor(c)))
            except Exception:
                palette_style.append(("BACKGROUND", (idx, 0), (idx, 0), colors.grey))
        palette_table.setStyle(TableStyle(palette_style))
        story.append(palette_table)
        story.append(Spacer(1, 6 * mm))

    # Section: Typography
    story.append(Paragraph("2. Typography", styles["Heading2TT"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(f"Heading font-family: {profile.font_heading}", styles["NormalSmall"]))
    story.append(Paragraph(f"Body font-family: {profile.font_body}", styles["NormalSmall"]))
    story.append(Spacer(1, 4 * mm))

    if profile.detected_fonts:
        story.append(Paragraph("Detected fonts from PDFs:", styles["NormalSmall"]))
        for f in profile.detected_fonts:
            story.append(Paragraph(f"- {f}", styles["NormalSmall"]))
        story.append(Spacer(1, 4 * mm))

    # Section: Logo
    story.append(Paragraph("3. Logo & Imagery", styles["Heading2TT"]))
    story.append(Spacer(1, 2 * mm))
    story.append(
        Paragraph(
            f"Logo path (detected from PDFs / images): {profile.logo_path or 'None detected'}",
            styles["NormalSmall"],
        )
    )
    story.append(Spacer(1, 4 * mm))

    # Section: Hex Colors from Text
    story.append(Paragraph("4. Hex Colors Found in Brand Guides", styles["Heading2TT"]))
    story.append(Spacer(1, 2 * mm))
    if profile.hex_colors_in_text:
        for h in profile.hex_colors_in_text:
            story.append(Paragraph(f"- {h}", styles["NormalSmall"]))
    else:
        story.append(Paragraph("No inline hex colors detected.", styles["NormalSmall"]))
    story.append(Spacer(1, 4 * mm))

    # Section: Usage
    story.append(Paragraph("5. Usage in Tri-Tender", styles["Heading2TT"]))
    story.append(Spacer(1, 2 * mm))
    usage_text = """
    This BrandProfile is used throughout Tri-Tender to ensure that all
    auto-generated tender outputs are visually aligned with your company identity,
    including letterheads, executive summaries, pricing schedules and charts.
    When your brand changes, simply upload new assets and regenerate the profile
    and Brand Book.
    """
    story.append(Paragraph(usage_text.strip(), styles["NormalSmall"]))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    encoded = base64.b64encode(pdf_bytes).decode("ascii")
    return f"data:application/pdf;base64,{encoded}"
