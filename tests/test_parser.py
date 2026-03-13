"""Tests for the Marp Markdown parser."""

from marp2pptx.converter import parse_marp, display_width, clean, est_lines


class TestDisplayWidth:
    def test_ascii_only(self):
        assert display_width("hello") == 5

    def test_cjk(self):
        assert display_width("日本語") == 6

    def test_mixed(self):
        assert display_width("Hello日本") == 9

    def test_empty(self):
        assert display_width("") == 0


class TestClean:
    def test_bold(self):
        assert clean("**bold**") == "bold"

    def test_italic(self):
        assert clean("*italic*") == "italic"

    def test_code(self):
        assert clean("`code`") == "code"

    def test_link(self):
        assert clean("[text](http://example.com)") == "text"

    def test_html_br(self):
        assert clean("line1<br>line2") == "line1\nline2"

    def test_html_tags(self):
        assert clean('<span class="tag">text</span>') == "text"

    def test_html_entities(self):
        assert clean("&amp; &lt;") == "& <"


class TestEstLines:
    def test_single_line(self):
        assert est_lines("short", 14, 500) == 1

    def test_wrapping(self):
        long_text = "a" * 200
        lines = est_lines(long_text, 14, 100)
        assert lines > 1


class TestParseMarp:
    def test_frontmatter_stripped(self):
        md = "---\nmarp: true\n---\n\n# Title\n"
        slides = parse_marp(md)
        assert len(slides) == 1
        assert slides[0]["elements"][0]["type"] == "h1"

    def test_slide_separator(self):
        md = "# Slide 1\n\n---\n\n# Slide 2\n"
        slides = parse_marp(md)
        assert len(slides) == 2

    def test_class_directive(self):
        md = "<!-- _class: lead -->\n# Title\n"
        slides = parse_marp(md)
        assert slides[0]["class"] == "lead"

    def test_bullets(self):
        md = "- item 1\n- item 2\n  - nested\n"
        slides = parse_marp(md)
        bullets = [e for e in slides[0]["elements"] if e["type"] == "bullets"]
        assert len(bullets) == 1
        assert len(bullets[0]["items"]) == 3
        assert bullets[0]["items"][2]["level"] == 1

    def test_code_block(self):
        md = "```python\nprint('hello')\n```\n"
        slides = parse_marp(md)
        code = [e for e in slides[0]["elements"] if e["type"] == "code"]
        assert len(code) == 1
        assert "print" in code[0]["text"]
        assert code[0]["arch"] is False

    def test_markdown_table(self):
        md = "| A | B |\n|---|---|\n| 1 | 2 |\n"
        slides = parse_marp(md)
        tables = [e for e in slides[0]["elements"] if e["type"] == "md_table"]
        assert len(tables) == 1
        assert tables[0]["rows"][0] == ["A", "B"]
        assert tables[0]["rows"][1] == ["1", "2"]

    def test_bg_image(self):
        md = "![bg right:30% 80%](logo.png)\n# Title\n"
        slides = parse_marp(md)
        assert slides[0]["bg_image"] == "logo.png"
        assert slides[0]["bg_pos"] == "right"
        assert slides[0]["bg_pct"] == 30

    def test_paragraph(self):
        md = "Some paragraph text\nwith continuation\n"
        slides = parse_marp(md)
        paras = [e for e in slides[0]["elements"] if e["type"] == "para"]
        assert len(paras) == 1

    def test_heading_levels(self):
        md = "# H1\n## H2\n### H3\n"
        slides = parse_marp(md)
        types = [e["type"] for e in slides[0]["elements"]]
        assert types == ["h1", "h2", "h3"]
