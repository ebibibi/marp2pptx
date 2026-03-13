"""Tests for font detection."""

from marp2pptx.fonts import find_monospace_font


class TestFindMonospaceFont:
    def test_returns_string_or_none(self):
        result = find_monospace_font()
        assert result is None or isinstance(result, str)

    def test_result_exists_if_found(self):
        from pathlib import Path
        result = find_monospace_font()
        if result is not None:
            assert Path(result).exists()
