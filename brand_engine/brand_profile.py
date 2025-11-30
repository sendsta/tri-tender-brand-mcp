from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class BrandProfile:
    """Canonical brand profile used across Tri-Tender."""

    name: Optional[str] = None
    logo_path: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    neutral_color: str = "#111827"
    background_color: str = "#F9FAFB"

    font_heading: str = "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    font_body: str = "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

    detected_colors: List[str] = field(default_factory=list)
    detected_fonts: List[str] = field(default_factory=list)
    hex_colors_in_text: List[str] = field(default_factory=list)

    chart_palette: List[str] = field(default_factory=list)

    def ensure_palette(self) -> None:
        """Ensure chart_palette has a nice sequence of colors."""
        if self.chart_palette:
            return

        base_colors = [
            c for c in [
                self.primary_color,
                self.secondary_color,
                self.accent_color,
                self.neutral_color,
            ] if c
        ]

        fallback = [
            "#2563EB",
            "#0EA5E9",
            "#22C55E",
            "#F97316",
            "#E11D48",
            "#A855F7",
        ]

        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for c in base_colors + fallback:
            if c and c not in seen:
                seen.add(c)
                deduped.append(c)

        self.chart_palette = deduped[:8]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BrandProfile":
        return cls(**data)
