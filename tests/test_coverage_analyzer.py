"""
Testes para execution/coverage_analyzer.py.

Combina testes unitários (AST, summary) com integração real via subprocesso.
"""
from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import pytest

from execution.coverage_analyzer import (
    CoverageAnalyzer,
    CoverageGap,
    _function_at_line,
    _index_functions,
)
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest


# ── Auxiliares ────────────────────────────────────────────────────────────────

def _make_test(code: str, target: str = "my_fn") -> GeneratedTest:
    return GeneratedTest(
        target_function=target,
        code=dedent(code).strip(),
        imports=[],
        coverage_hints=[],
    )


_SAMPLE_SOURCE = dedent("""\
    def add(a, b):
        return a + b

    def subtract(a, b):
        if b > a:
            return 0
        return a - b

    def unused():
        return 99
""")


# ── _index_functions ──────────────────────────────────────────────────────────

def test_index_functions_top_level() -> None:
    spans = _index_functions(_SAMPLE_SOURCE)
    names = [s.name for s in spans]
    assert "add" in names
    assert "subtract" in names
    assert "unused" in names


def test_index_functions_class_methods() -> None:
    source = dedent("""\
        class Calc:
            def multiply(self, a, b):
                return a * b
    """)
    spans = _index_functions(source)
    assert len(spans) == 1
    assert spans[0].name == "Calc.multiply"
    assert spans[0].start_line == 2


def test_function_at_line() -> None:
    spans = _index_functions(_SAMPLE_SOURCE)
    assert _function_at_line(spans, 2) == "add"
    assert _function_at_line(spans, 6) == "subtract"
    assert _function_at_line(spans, 999) == "<module>"


# ── CoverageGap ───────────────────────────────────────────────────────────────

def test_coverage_gap_dataclass() -> None:
    gap = CoverageGap(
        file_path="calc.py",
        function_name="subtract",
        uncovered_lines=[6, 7],
    )
    assert gap.file_path == "calc.py"
    assert gap.uncovered_lines == [6, 7]


# ── generate_summary (sem dados) ─────────────────────────────────────────────

def test_generate_summary_without_run() -> None:
    analyzer = CoverageAnalyzer(
        _make_test("def test_x(): pass"),
        "nonexistent.py",
    )
    summary = analyzer.generate_summary()
    assert summary["meets_threshold"] is False
    assert summary["line_coverage_percent"] == 0.0
    assert "error" in summary


# ── Integração real ───────────────────────────────────────────────────────────

@pytest.fixture()
def partial_coverage_module(tmp_path):
    """Módulo com função parcialmente coberta por um teste."""
    mod = tmp_path / "sample_mod.py"
    mod.write_text(_SAMPLE_SOURCE, encoding="utf-8")

    test_code = dedent("""\
        from sample_mod import add, subtract

        def test_add():
            assert add(1, 2) == 3

        def test_subtract_normal():
            assert subtract(5, 2) == 3
    """)
    test = _make_test(test_code, target="sample_mod")
    return str(mod), test


def test_run_executes_tests(partial_coverage_module) -> None:
    source_path, test = partial_coverage_module
    parent = str(Path(source_path).parent)
    analyzer = CoverageAnalyzer(test, source_path, pythonpath=[parent])
    result = analyzer.run()
    assert result.passed
    assert result.num_passed >= 2


def test_find_gaps_detects_uncovered_lines(partial_coverage_module) -> None:
    source_path, test = partial_coverage_module
    parent = str(Path(source_path).parent)
    analyzer = CoverageAnalyzer(
        test, source_path,
        target_function="subtract",
        pythonpath=[parent],
        threshold=100.0,
    )
    analyzer.run()
    gaps = analyzer.find_gaps()

    assert len(gaps) >= 1
    gap = gaps[0]
    assert gap.function_name == "subtract"
    assert len(gap.uncovered_lines) >= 1


def test_find_gaps_filters_by_target_function(partial_coverage_module) -> None:
    source_path, test = partial_coverage_module
    parent = str(Path(source_path).parent)
    analyzer = CoverageAnalyzer(
        test, source_path,
        target_function="add",
        pythonpath=[parent],
        threshold=100.0,
    )
    analyzer.run()
    gaps = analyzer.find_gaps()
    assert all(g.function_name == "add" for g in gaps)


def test_generate_summary_structure(partial_coverage_module) -> None:
    source_path, test = partial_coverage_module
    parent = str(Path(source_path).parent)
    analyzer = CoverageAnalyzer(
        test, source_path,
        target_function="subtract",
        pythonpath=[parent],
        threshold=80.0,
    )
    analyzer.run()
    summary = analyzer.generate_summary()

    assert "line_coverage_percent" in summary
    assert "threshold_percent" in summary
    assert "meets_threshold" in summary
    assert "gaps" in summary
    assert "uncovered_branches" in summary
    assert "uncovered_functions" in summary
    assert isinstance(summary["gaps"], list)


def test_generate_summary_json_valid(partial_coverage_module) -> None:
    source_path, test = partial_coverage_module
    parent = str(Path(source_path).parent)
    analyzer = CoverageAnalyzer(test, source_path, pythonpath=[parent])
    analyzer.run()
    raw = analyzer.generate_summary_json()
    parsed = json.loads(raw)
    assert "gaps" in parsed


def test_meets_threshold(partial_coverage_module) -> None:
    source_path, test = partial_coverage_module
    parent = str(Path(source_path).parent)
    analyzer = CoverageAnalyzer(
        test, source_path,
        pythonpath=[parent],
        threshold=0.0,
    )
    analyzer.run()
    assert analyzer.meets_threshold()


def test_uncovered_functions_detected(tmp_path) -> None:
    mod = tmp_path / "mod.py"
    mod.write_text(dedent("""\
        def covered():
            return 1

        def never_called():
            return 2
    """), encoding="utf-8")

    test = _make_test(dedent("""\
        from mod import covered

        def test_covered():
            assert covered() == 1
    """), target="mod")

    analyzer = CoverageAnalyzer(
        test, str(mod),
        pythonpath=[str(tmp_path)],
        threshold=100.0,
    )
    analyzer.run()
    summary = analyzer.generate_summary()
    fn_names = [f["function_name"] for f in summary["uncovered_functions"]]
    assert "never_called" in fn_names


# ── Integração com FunctionContext ─────────────────────────────────────────────

def test_context_prompt_includes_coverage_gaps() -> None:
    ctx = FunctionContext(
        function_name="subtract",
        qualified_name="subtract",
        symbol_type="function",
        file_path="sample_mod.py",
        code="def subtract(a, b): ...",
        coverage_gaps=[{
            "file_path": "sample_mod.py",
            "function_name": "subtract",
            "uncovered_lines": [6, 7],
        }],
        coverage_summary={
            "line_coverage_percent": 60.0,
            "threshold_percent": 80.0,
            "meets_threshold": False,
            "uncovered_branches": [{
                "file_path": "sample_mod.py",
                "function_name": "subtract",
                "from_line": 6,
                "to_line": 8,
            }],
            "uncovered_functions": [{
                "file_path": "sample_mod.py",
                "function_name": "unused",
            }],
        },
    )
    prompt = ctx.to_prompt_block()
    assert "Lacunas de cobertura" in prompt
    assert "subtract" in prompt
    assert "Branches não cobertos" in prompt
    assert "Funções sem cobertura" in prompt
    assert "unused" in prompt
