from __future__ import annotations

from ingest.models.ExtractedSymbol import ExtractedSymbol
from ingest.symbol_filter import filter_symbols_for_tests, should_generate_tests
from schemas.prompt_utils import compact_rag_snippet


def _symbol(name: str, *, file_path: str = "mockes/exemplo.py") -> ExtractedSymbol:
    return ExtractedSymbol(
        symbol_type="function",
        name=name,
        qualified_name=name,
        class_name=None,
        file_path=file_path,
        source_code=f"def {name}(): pass",
        docstring=None,
        imports=[],
        dependencies=[],
        exceptions=[],
        decorators=[],
        branches=0,
        edge_cases=[],
    )


def test_skip_module_level_main() -> None:
    assert not should_generate_tests(_symbol("main"))
    assert should_generate_tests(_symbol("soma"))


def test_skip_demo_files() -> None:
    assert not should_generate_tests(
        _symbol("helper", file_path="mockes/embedding_demo.py"),
    )


def test_filter_symbols_for_tests() -> None:
    symbols = [
        _symbol("main"),
        _symbol("soma"),
        _symbol("run", file_path="mockes/embedding_demo.py"),
    ]
    kept = filter_symbols_for_tests(symbols)
    assert [s.name for s in kept] == ["soma"]


def test_compact_rag_snippet_extracts_code() -> None:
    raw = "symbol: foo\ntype: function\ncode:\ndef foo(): return 1"
    compact = compact_rag_snippet(raw, max_chars=500)
    assert compact == "def foo(): return 1"


def test_compact_rag_snippet_truncates() -> None:
    text = "x" * 100
    compact = compact_rag_snippet(text, max_chars=20)
    assert compact.endswith("(truncado)")
    assert len(compact) < 100
