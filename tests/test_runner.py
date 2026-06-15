"""
Testes para execution/runner.py e execution/coverage_format.py.

Usa chamadas reais de subprocesso do pytest em código de teste trivial em memória.
Sem necessidade de mocking — isso valida o funcionamento real da execução.
"""
from __future__ import annotations

from textwrap import dedent

import pytest

from execution.coverage_format import format_ranges, parse_missing_ranges
from execution.runner import RunResult, TestRunner, _parse_pytest_counts
from schemas.outputs import GeneratedTest


# ── Auxiliares ────────────────────────────────────────────────────────────────

def _make_test(code: str, target: str = "my_fn") -> GeneratedTest:
    return GeneratedTest(
        target_function=target,
        code=dedent(code).strip(),
        imports=[],
        coverage_hints=[],
    )


@pytest.fixture()
def runner() -> TestRunner:
    return TestRunner()


# ── _parse_pytest_counts ──────────────────────────────────────────────────────

def test_parse_counts_all_passed() -> None:
    output = "3 passed in 0.42s"
    assert _parse_pytest_counts(output) == (3, 0, 0)


def test_parse_counts_mixed() -> None:
    output = "2 passed, 1 failed in 0.10s"
    assert _parse_pytest_counts(output) == (2, 1, 0)


def test_parse_counts_errors() -> None:
    output = "0 passed, 1 error in 0.05s"
    p, f, e = _parse_pytest_counts(output)
    assert e == 1


def test_parse_counts_empty_output() -> None:
    assert _parse_pytest_counts("") == (0, 0, 0)


# ── TestRunner — testes que passam ────────────────────────────────────────────

def test_runner_passes_trivial_test(runner) -> None:
    test = _make_test("""\
        def test_always_passes():
            assert 1 + 1 == 2
    """)
    result = runner.run(test)
    assert result.passed
    assert result.exit_code == 0
    assert result.num_passed >= 1


def test_runner_multiple_passing_tests(runner) -> None:
    test = _make_test("""\
        def test_a(): assert True
        def test_b(): assert 2 * 3 == 6
        def test_c(): assert "hello".upper() == "HELLO"
    """)
    result = runner.run(test)
    assert result.passed
    assert result.num_passed == 3


def test_runner_captures_stdout(runner) -> None:
    test = _make_test("""\
        def test_print():
            print("hello from test")
            assert True
    """)
    result = runner.run(test)
    assert result.passed
    # stdout capturado (pode aparecer em result.stdout com a flag -s;
    # sem ela, é capturado pelo pytest — apenas garante que não trave)


# ── TestRunner — testes falhando ──────────────────────────────────────────────

def test_runner_detects_assertion_failure(runner) -> None:
    test = _make_test("""\
        def test_fails():
            assert 1 == 2, "intentional failure"
    """)
    result = runner.run(test)
    assert not result.passed
    assert result.exit_code != 0
    assert result.num_failed >= 1


def test_runner_detects_import_error(runner) -> None:
    test = _make_test("""\
        from totally_nonexistent_module_xyz import something

        def test_never_reached():
            assert True
    """)
    result = runner.run(test)
    assert not result.passed


def test_runner_detects_exception_in_test(runner) -> None:
    test = _make_test("""\
        def test_raises_unexpectedly():
            raise RuntimeError("boom")
    """)
    result = runner.run(test)
    assert not result.passed


# ── TestRunner — auxiliares de saída ──────────────────────────────────────────

def test_run_result_output_combines_stdout_stderr(runner) -> None:
    test = _make_test("""\
        def test_fail():
            assert False
    """)
    result = runner.run(test)
    # a propriedade de saída (output) não deve estar vazia para um teste falho
    assert result.output.strip() != ""


def test_run_result_failure_summary_non_empty_on_fail(runner) -> None:
    test = _make_test("""\
        def test_fail():
            assert 1 == 99
    """)
    result = runner.run(test)
    assert not result.passed
    assert result.failure_summary.strip() != ""


def test_run_result_failure_summary_empty_on_pass(runner) -> None:
    test = _make_test("""\
        def test_pass(): assert True
    """)
    result = runner.run(test)
    assert result.failure_summary == ""


def test_runner_timeout_returns_failed_result(runner) -> None:
    test = _make_test("""\
        import time

        def test_slow():
            time.sleep(10)
    """)
    result = runner.run(test, timeout=1)
    assert not result.passed
    assert result.exit_code == -1
    assert "tempo limite" in result.stderr.lower()


# ── parse_missing_ranges ──────────────────────────────────────────────────────

def test_parse_missing_ranges_single_lines() -> None:
    assert parse_missing_ranges("8, 12, 22") == [8, 12, 22]


def test_parse_missing_ranges_range() -> None:
    assert parse_missing_ranges("12-14") == [12, 13, 14]


def test_parse_missing_ranges_mixed() -> None:
    result = parse_missing_ranges("8, 12-14, 22")
    assert result == [8, 12, 13, 14, 22]


def test_parse_missing_ranges_empty() -> None:
    assert parse_missing_ranges("") == []


def test_parse_missing_ranges_deduplicates() -> None:
    assert parse_missing_ranges("8, 8, 9") == [8, 9]


# ── format_ranges ─────────────────────────────────────────────────────────────

def test_format_ranges_single_numbers() -> None:
    assert format_ranges([8, 12, 22]) == "8, 12, 22"


def test_format_ranges_consecutive_compresses() -> None:
    assert format_ranges([12, 13, 14]) == "12-14"


def test_format_ranges_mixed() -> None:
    assert format_ranges([8, 12, 13, 14, 22]) == "8, 12-14, 22"


def test_format_ranges_empty() -> None:
    assert format_ranges([]) == ""