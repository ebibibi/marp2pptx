"""marp2pptx — Convert Marp Markdown slides to PowerPoint with auto-sizing fonts."""

from .converter import convert, parse_marp, check_overlaps
from .config import load_config, Config

__all__ = ["convert", "parse_marp", "check_overlaps", "load_config", "Config"]
