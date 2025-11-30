from __future__ import annotations

import os
import re
from typing import List, Tuple

from PIL import Image


HEX_COLOR_PATTERN = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b")


def extract_hex_colors_from_text(text: str) -> List[str]:
    """Find hex color codes in plain text (`#RRGGBB` / `#RGB`)."""
    matches = HEX_COLOR_PATTERN.findall(text or "")
    # Normalise to uppercase
    return sorted(set(m.upper() for m in matches))


def image_dominant_colors(image_path: str, top_n: int = 5) -> List[str]:
    """
    Compute dominant colors from an image using a simple histogram.

    Returns:
        List of hex color strings.
    """
    if not os.path.exists(image_path):
        return []

    img = Image.open(image_path).convert("RGB")
    # Downscale for performance
    img = img.resize((128, 128))

    colors = img.getcolors(maxcolors=128 * 128)
    if not colors:
        return []

    # Sort by frequency descending
    colors.sort(key=lambda x: x[0], reverse=True)
    top = colors[:top_n]
    hex_colors = [rgb_to_hex(c[1]) for c in top]
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for h in hex_colors:
        if h not in seen:
            seen.add(h)
            deduped.append(h)
    return deduped


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def safe_filename(name: str) -> str:
    """Strip weird characters from a filename."""
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name.strip())
