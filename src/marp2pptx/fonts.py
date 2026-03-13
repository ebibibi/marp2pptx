"""Cross-platform CJK monospace font detection for ASCII art rendering."""

import shutil
import subprocess
from pathlib import Path


# Candidate fonts in preference order.
# Each entry: (font_path_patterns_by_platform, name_for_logging)
_CANDIDATES = [
    # IPAGothic — best CJK monospace, common on Linux
    [
        "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
        "/usr/share/fonts/ipa-gothic/ipag.ttf",  # Fedora
    ],
    # Noto Sans Mono CJK
    [
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/noto-cjk/NotoSansCJKjp-Regular.otf",
    ],
    # MS Gothic (Windows)
    [
        "C:/Windows/Fonts/msgothic.ttc",
    ],
    # macOS — Osaka Mono or Hiragino
    [
        "/System/Library/Fonts/Osaka.ttf",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/Library/Fonts/Osaka.ttf",
    ],
    # DejaVu Sans Mono (fallback, no CJK but widely available)
    [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf",
    ],
]


def find_monospace_font() -> str | None:
    """Find the best available monospace font with CJK support.

    Returns the font file path, or None if no suitable font is found.
    """
    for candidate_group in _CANDIDATES:
        for path_str in candidate_group:
            if Path(path_str).exists():
                return path_str

    # Last resort: try fc-match on Linux
    if shutil.which("fc-match"):
        try:
            result = subprocess.run(
                ["fc-match", "-f", "%{file}", "monospace:lang=ja"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                path = result.stdout.strip()
                if Path(path).exists():
                    return path
        except (subprocess.TimeoutExpired, OSError):
            pass

    return None
