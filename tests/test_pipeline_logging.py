from __future__ import annotations

from pathlib import Path

import pytest

from agents.services.pipeline_logging import log_ingest_selection
from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from parsers.source.path_filters import ExcludedPythonFile, ScanResult
from parsers.source.symbol_filter import FilteredSymbol, SymbolFilterResult, SymbolFilterStats


def _symbol(name: str, *, symbol_type: str = "function") -> ExtractedSymbol:
    return ExtractedSymbol(
        symbol_type=symbol_type,
        name=name,
        qualified_name=name,
        class_name=None,
        file_path=f"{name}.py",
        source_code=f"def {name}(): pass",
        imports=[],
        dependencies=[],
        exceptions=[],
        decorators=[],
        docstring=None,
        branches=0,
        edge_cases=[],
    )


def test_log_ingest_selection_lists_files_and_symbols(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level("INFO")
    src = tmp_path / "src"
    src.mkdir()
    included = src / "foo.py"
    included.touch()

    scan_result = ScanResult(
        files=(included,),
        total_py_found=2,
        excluded=1,
        excluded_files=(
            ExcludedPythonFile(path="test_foo.py", reason="glob:test_*.py"),
        ),
    )
    filter_result = SymbolFilterResult(
        kept=[_symbol("foo")],
        stats=SymbolFilterStats(
            extracted_total=2,
            filtered_total=1,
            removed_container_class=1,
        ),
        filtered=(
            FilteredSymbol(
                qualified_name="Bar",
                symbol_type="class",
                file_path="bar.py",
                reason="container_class",
            ),
        ),
    )

    log_ingest_selection(
        src,
        scan_result,
        filter_result,
        selection_artifact=tmp_path / "ingest_selection.json",
    )

    messages = [record.message for record in caplog.records]
    assert any("[arquivo +] foo.py" in msg for msg in messages)
    assert any("[arquivo -] test_foo.py (glob:test_*.py)" in msg for msg in messages)
    assert any("[símbolo +] foo (function)" in msg for msg in messages)
    assert any("[símbolo -] Bar (class) — container_class" in msg for msg in messages)
    assert any("ingest_selection.json" in msg for msg in messages)
