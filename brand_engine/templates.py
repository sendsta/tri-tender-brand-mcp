from __future__ import annotations

from .brand_profile import BrandProfile


def generate_letterhead_template(profile: BrandProfile) -> str:
    profile.ensure_palette()

    primary = profile.primary_color or "#0B1120"
    secondary = profile.secondary_color or "#2563EB"
    accent = profile.accent_color or "#0EA5E9"
    bg = profile.background_color or "#F9FAFB"
    neutral = profile.neutral_color or "#111827"

    logo_html = ""
    if profile.logo_path:
        # In FastMCP Cloud this is typically a file path; the Tri-Tender client
        # can rewrite/serve this path as a URL if needed.
        logo_html = f'<img src="{profile.logo_path}" alt="Logo" class="brand-logo" />'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{{{{ title | default("Tri-Tender Document") }}}}</title>
  <style>
    :root {{
      --brand-primary: {primary};
      --brand-secondary: {secondary};
      --brand-accent: {accent};
      --brand-neutral: {neutral};
      --brand-bg: {bg};

      --font-heading: {profile.font_heading};
      --font-body: {profile.font_body};
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      padding: 0;
      background: var(--brand-bg);
      font-family: var(--font-body);
      color: var(--brand-neutral);
    }}

    .page {{
      max-width: 960px;
      margin: 24px auto;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
      overflow: hidden;
      border: 1px solid rgba(15, 23, 42, 0.06);
    }}

    .letterhead-header {{
      display: flex;
      align-items: center;
      padding: 20px 28px;
      background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
      color: white;
    }}

    .brand-logo {{
      max-height: 56px;
      max-width: 160px;
      object-fit: contain;
      margin-right: 18px;
      border-radius: 8px;
      background: rgba(255,255,255,0.06);
      padding: 6px 10px;
    }}

    .brand-title-block {{
      display: flex;
      flex-direction: column;
    }}

    .brand-name {{
      font-family: var(--font-heading);
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.02em;
    }}

    .brand-subtitle {{
      font-size: 12px;
      opacity: 0.9;
      margin-top: 3px;
    }}

    .header-accent-bar {{
      height: 4px;
      background: linear-gradient(90deg, var(--brand-accent), var(--brand-secondary));
    }}

    .content {{
      padding: 28px 32px 32px 32px;
      font-size: 14px;
      line-height: 1.6;
    }}

    .content h1, .content h2, .content h3 {{
      font-family: var(--font-heading);
      color: var(--brand-primary);
      margin-top: 0;
    }}

    .meta-row {{
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #6B7280;
      margin-bottom: 14px;
      border-bottom: 1px solid #E5E7EB;
      padding-bottom: 10px;
    }}

    .meta-block {{
      display: flex;
      flex-direction: column;
    }}

    .meta-label {{
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 600;
      font-size: 10px;
      color: #9CA3AF;
      margin-bottom: 2px;
    }}

    .meta-value {{
      font-size: 11px;
    }}

    .footer {{
      padding: 12px 28px 20px 28px;
      background: #F3F4F6;
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      color: #6B7280;
      border-top: 1px solid #E5E7EB;
    }}

    .footer a {{
      color: var(--brand-secondary);
      text-decoration: none;
    }}

    @media print {{
      body {{
        background: #ffffff;
      }}
      .page {{
        box-shadow: none;
        margin: 0;
        border-radius: 0;
        border: none;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header class="letterhead-header">
      <div class="logo-wrapper">
        {logo_html}
      </div>
      <div class="brand-title-block">
        <div class="brand-name">{{{{ company_name | default("Your Company Name") }}}}</div>
        <div class="brand-subtitle">{{{{ company_tagline | default("Professional Tender Response Partner") }}}}</div>
      </div>
    </header>
    <div class="header-accent-bar"></div>
    <main class="content">
      <div class="meta-row">
        <div class="meta-block">
          <div class="meta-label">Document</div>
          <div class="meta-value">{{{{ document_title | default("Tender Document") }}}}</div>
        </div>
        <div class="meta-block">
          <div class="meta-label">Tender</div>
          <div class="meta-value">{{{{ tender_ref | default("BID / RFQ NUMBER") }}}}</div>
        </div>
        <div class="meta-block">
          <div class="meta-label">Date</div>
          <div class="meta-value">{{{{ issue_date | default("YYYY-MM-DD") }}}}</div>
        </div>
      </div>

      <!-- BODY SLOT -->
      {{{{ body_html | safe }}}}
    </main>
    <footer class="footer">
      <div class="footer-left">
        {{{{ company_footer_left | default("Physical Address • City • Country") }}}}
      </div>
      <div class="footer-right">
        {{{{ company_footer_right | default("Tel: +27 00 000 0000 • Email: info@example.com • www.example.com") }}}}
      </div>
    </footer>
  </div>
</body>
</html>
"""


def wrap_body_in_letterhead(profile: BrandProfile, body_html: str, title: str = "Tri-Tender Document") -> str:
    """
    Render a full HTML document by injecting `body_html` into the letterhead template.
    """
    # For now we use simple string replacement of a placeholder. In a more advanced
    # setup you can plug any template engine (Jinja, etc.).
    template = generate_letterhead_template(profile)
    return template.replace("{{{{ body_html | safe }}}}", body_html).replace(
        "{{{{ title | default(\"Tri-Tender Document\") }}}}", title
    )


def generate_graph_style_guide(profile: BrandProfile) -> dict:
    """
    Returns a graph style guide based on the brand profile.
    """
    profile.ensure_palette()
    return {
        "series_colors": profile.chart_palette,
        "background": profile.background_color or "#FFFFFF",
        "grid_color": "#E5E7EB",
        "axis": {
            "color": "#4B5563",
            "width": 1,
        },
        "label": {
            "color": "#111827",
            "font_family": profile.font_body,
            "font_size": 12,
        },
        "title": {
            "color": profile.primary_color or "#0B1120",
            "font_family": profile.font_heading,
            "font_size": 16,
            "font_weight": 700,
        },
        "tooltip": {
            "background": "#111827",
            "color": "#F9FAFB",
        },
    }
