"""Design configuration loading with YAML support.

Resolution order:
1. <input>.yaml  (same name as the .md file)
2. marp2pptx.yaml in the same directory
3. Built-in default.yaml
"""

from pathlib import Path

import yaml
from pptx.dml.color import RGBColor


_DEFAULT_YAML = Path(__file__).parent / "default.yaml"


def _hex_to_rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _deep_merge(base: dict, override: dict) -> dict:
    """Merge override into base, returning a new dict."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config(md_path: Path) -> "Config":
    """Load and merge configuration, returning a Config object."""
    with open(_DEFAULT_YAML, encoding="utf-8") as f:
        base = yaml.safe_load(f)

    # Look for user overrides
    candidates = [
        md_path.with_suffix(".yaml"),
        md_path.parent / "marp2pptx.yaml",
    ]
    for candidate in candidates:
        if candidate.exists():
            with open(candidate, encoding="utf-8") as f:
                user = yaml.safe_load(f)
            if user:
                base = _deep_merge(base, user)
            break

    return Config(base)


class Config:
    """Parsed design configuration with typed accessors."""

    def __init__(self, data: dict):
        self._data = data
        slide = data["slide"]
        self.slide_w: float = slide["width"]
        self.slide_h: float = slide["height"]
        self.margin: float = slide["margin"]

        c = data["colors"]
        self.accent = _hex_to_rgb(c["accent"])
        self.accent_dark = _hex_to_rgb(c["accent_dark"])
        self.text_color = _hex_to_rgb(c["text"])
        self.gray = _hex_to_rgb(c["gray"])
        self.white = _hex_to_rgb(c["white"])
        self.code_bg = _hex_to_rgb(c["code_bg"])
        self.table_header_bg = c["table_header_bg"].lstrip("#")

        self.tag_colors: dict[str, RGBColor] = {
            k: _hex_to_rgb(v) for k, v in data.get("tag_colors", {}).items()
        }

        fonts = data["fonts"]
        self.font: str = fonts["main"]
        self.mono: str = fonts["mono"]

        raw_ranges = data["font_ranges"]
        self.font_ranges: dict[str, tuple[int, int, int]] = {}
        for key, vals in raw_ranges.items():
            mapped_key = "" if key == "default" else key
            self.font_ranges[mapped_key] = tuple(vals)
