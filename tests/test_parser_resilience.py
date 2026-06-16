from __future__ import annotations

from pathlib import Path

from parsers.source.parser import parse_repository, parse_repository_symbols


def test_parse_repository_skips_syntax_error(tmp_path: Path) -> None:
    root = tmp_path / "pkg"
    root.mkdir()
    (root / "ok.py").write_text("def good():\n    return 1\n", encoding="utf-8")
    (root / "bad.py").write_text('    """orphan docstring"""\n', encoding="utf-8")

    parsed = list(parse_repository(str(root)))
    symbols = list(parse_repository_symbols(str(root)))

    assert len(parsed) == 1
    assert parsed[0].path.endswith("ok.py")
    assert len(symbols) == 1
    assert symbols[0].qualified_name == "good"
