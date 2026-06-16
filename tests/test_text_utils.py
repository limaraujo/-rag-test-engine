from __future__ import annotations

from pathlib import Path

from parsers.source.text_utils import read_source_text, strip_utf8_bom


def test_strip_utf8_bom_removes_leading_bom() -> None:
    assert strip_utf8_bom("\ufeffimport x") == "import x"
    assert strip_utf8_bom("import x") == "import x"


def test_read_source_text_strips_file_bom(tmp_path: Path) -> None:
    path = tmp_path / "sample.py"
    path.write_bytes(b"\xef\xbb\xbfx = 1\n")
    assert read_source_text(path) == "x = 1\n"


def test_get_ast_from_file_accepts_bom(tmp_path: Path) -> None:
    import ast

    from parsers.source.ast_utils import get_ast_from_file

    path = tmp_path / "mod.py"
    path.write_bytes(b"\xef\xbb\xbfdef foo():\n    return 1\n")
    tree = get_ast_from_file(str(path))
    assert isinstance(tree, ast.Module)
