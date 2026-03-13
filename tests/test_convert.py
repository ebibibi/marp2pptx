"""Tests for the full conversion pipeline."""

import tempfile
from pathlib import Path

from marp2pptx import convert, check_overlaps


FIXTURES = Path(__file__).parent / "fixtures"


class TestConvert:
    def test_simple_conversion(self):
        md = FIXTURES / "simple.md"
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "output.pptx"
            result_path, count = convert(md, out)
            assert result_path == out
            assert count == 4
            assert out.exists()
            assert out.stat().st_size > 0

    def test_default_output_path(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            md = td / "slides.md"
            md.write_text(
                "---\nmarp: true\n---\n\n# Title\n\n---\n\n# Slide 2\n"
            )
            result_path, count = convert(md)
            assert result_path == td / "slides.pptx"
            assert count == 2

    def test_overlap_check(self):
        md = FIXTURES / "simple.md"
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "output.pptx"
            convert(md, out)
            issues = check_overlaps(out)
            assert isinstance(issues, list)
