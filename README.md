# marp2pptx

Convert [Marp](https://marp.app/) Markdown slides to PowerPoint (.pptx) with **auto-sizing fonts**.

## Features

- **Auto-sizing**: Finds the largest font size that fits without overflow
- **CJK support**: Full-width / half-width aware text measurement
- **ASCII art**: Renders code blocks marked with `arch-box` as pixel-perfect images using monospace fonts
- **Tables**: HTML and Markdown table support with wrapping-aware height estimation
- **Design config**: Externalize colors, fonts, and font ranges to a YAML file
- **Overlap detection**: Self-check that warns about overlapping shapes

## Installation

```bash
pip install git+https://github.com/ebibibi/marp2pptx.git
```

### Font for ASCII art

For ASCII art rendering with CJK characters, install a monospace CJK font:

```bash
# Ubuntu/Debian
sudo apt install fonts-ipafont-gothic

# Fedora
sudo dnf install ipa-gothic-fonts
```

The tool auto-detects available fonts (IPAGothic, Noto Sans Mono CJK, MS Gothic, Osaka, DejaVu).

## Usage

```bash
# Basic
marp2pptx slides.md

# Custom output path
marp2pptx slides.md -o presentation.pptx

# Skip overlap check
marp2pptx slides.md --no-check
```

Or as a Python module:

```bash
python -m marp2pptx slides.md
```

### Python API

```python
from marp2pptx import convert

output_path, slide_count = convert("slides.md")
```

## Design Configuration

Create a YAML file to customize the design. The tool looks for config in this order:

1. `<input>.yaml` (e.g., `slides.yaml` for `slides.md`)
2. `marp2pptx.yaml` in the same directory
3. Built-in defaults

Example `slides.yaml`:

```yaml
colors:
  accent: "#FF6600"
  text: "#333333"

fonts:
  main: "Arial"
  mono: "Courier New"

font_ranges:
  default: [40, 14, 36]  # [title_max, body_min, body_max]
  small: [36, 12, 28]
```

See [`default.yaml`](src/marp2pptx/default.yaml) for all available options.

## Supported Markdown

- Marp frontmatter (`---` / `marp: true`)
- Slide separators (`---`)
- Class directives (`<!-- _class: lead -->`)
- Background images (`![bg right:30% 80%](image.png)`)
- Headings (h1–h3)
- Bullet lists (nested)
- Markdown and HTML tables
- Code blocks
- ASCII art blocks (`<div class="arch-box">`)
- Inline formatting: **bold**, *italic*, `code`, links, `<span class="tag-xxx">`

## License

MIT
