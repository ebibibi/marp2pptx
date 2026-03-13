"""Tests for config loading."""

import tempfile
from pathlib import Path

from pptx.dml.color import RGBColor

from marp2pptx.config import load_config, Config, _deep_merge


class TestDeepMerge:
    def test_flat(self):
        result = _deep_merge({"a": 1, "b": 2}, {"b": 3, "c": 4})
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_nested(self):
        base = {"colors": {"accent": "#000", "text": "#111"}}
        override = {"colors": {"accent": "#FFF"}}
        result = _deep_merge(base, override)
        assert result["colors"]["accent"] == "#FFF"
        assert result["colors"]["text"] == "#111"

    def test_no_mutation(self):
        base = {"a": {"b": 1}}
        override = {"a": {"c": 2}}
        _deep_merge(base, override)
        assert "c" not in base["a"]


class TestLoadConfig:
    def test_defaults(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            f.write(b"# test")
            md_path = Path(f.name)
        try:
            cfg = load_config(md_path)
            assert isinstance(cfg, Config)
            assert cfg.slide_w == 13.33
            assert cfg.slide_h == 7.5
            assert cfg.font == "Meiryo"
            assert cfg.mono == "Consolas"
            assert isinstance(cfg.accent, RGBColor)
        finally:
            md_path.unlink()

    def test_user_override(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            md = td / "slides.md"
            md.write_text("# test")
            yaml = td / "slides.yaml"
            yaml.write_text('fonts:\n  main: "Arial"\n')

            cfg = load_config(md)
            assert cfg.font == "Arial"
            assert cfg.mono == "Consolas"  # unchanged

    def test_font_ranges(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            f.write(b"# test")
            md_path = Path(f.name)
        try:
            cfg = load_config(md_path)
            assert "" in cfg.font_ranges  # "default" mapped to ""
            assert "lead" in cfg.font_ranges
            assert len(cfg.font_ranges[""]) == 3
        finally:
            md_path.unlink()
