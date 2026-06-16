from __future__ import annotations

from agents.services.suite_metrics import (
    build_suite_metrics,
    format_suite_metrics_table,
    is_suite_executable,
)
from execution.runner import RunResult, SuiteValidationResult
from parsers.source.symbol_filter import SymbolFilterStats
from schemas.pipeline import PipelineStats, SymbolRunRecord


def _run_result(
    *,
    passed: bool = True,
    passed_n: int = 1,
    failed_n: int = 0,
    errors_n: int = 0,
    exit_code: int = 0,
) -> RunResult:
    return RunResult(
        passed=passed,
        exit_code=exit_code,
        stdout="",
        stderr="",
        duration_seconds=0.1,
        test_file="t.py",
        num_passed=passed_n,
        num_failed=failed_n,
        num_errors=errors_n,
    )


def test_is_suite_executable_rejects_collection_errors() -> None:
    result = _run_result(passed=False, passed_n=0, failed_n=0, errors_n=1, exit_code=2)
    assert is_suite_executable(result) is False


def test_is_suite_executable_accepts_failed_assertions() -> None:
    result = _run_result(passed=False, passed_n=0, failed_n=2, errors_n=0, exit_code=1)
    assert is_suite_executable(result) is True


def test_build_suite_metrics_rates() -> None:
    stats = PipelineStats(
        ok=2,
        failed=1,
        skipped=1,
        symbol_runs=[
            SymbolRunRecord(
                qualified_name="a",
                file_path="pkg/a.py",
                suite_executable=True,
                first_generation_passed=True,
                passed=True,
                tests_collected=2,
                pytest_num_passed=2,
                current_coverage_percent=80.0,
                current_branch_coverage_percent=50.0,
                llm_calls=1,
                duration_seconds=1.5,
            ),
            SymbolRunRecord(
                qualified_name="b",
                file_path="pkg/b.py",
                suite_executable=True,
                first_generation_passed=False,
                passed=True,
                repaired=True,
                tests_collected=1,
                pytest_num_passed=1,
                current_coverage_percent=100.0,
                llm_calls=2,
                duration_seconds=2.5,
            ),
            SymbolRunRecord(
                qualified_name="c",
                file_path="pkg/c.py",
                suite_executable=False,
                stop_reason="error:syntax",
                llm_calls=0,
                duration_seconds=0.2,
            ),
            SymbolRunRecord(
                qualified_name="d",
                file_path="pkg/d.py",
                suite_executable=False,
                stop_reason="tests_failed",
                tests_collected=1,
                pytest_num_failed=1,
                llm_calls=1,
                duration_seconds=1.0,
            ),
        ],
    )
    metrics = build_suite_metrics(
        stats,
        filter_stats=SymbolFilterStats(extracted_total=5, filtered_total=1),
        token_usage={
            "by_symbol": {
                "a": {"total_tokens": 100, "estimated_cost": 0.001},
                "b": {"total_tokens": 200, "estimated_cost": 0.002},
            }
        },
        validation=SuiteValidationResult(
            passed=True,
            exit_code=0,
            stdout="",
            stderr="",
            duration_seconds=0.5,
            tests_dir="tests",
            num_passed=3,
            num_failed=0,
        ),
    )

    assert metrics["symbols_processed"] == 4
    assert metrics["rates"]["valid_generation_percent"] == 50.0
    assert metrics["rates"]["first_attempt_success_percent"] == 25.0
    assert metrics["rates"]["approval_percent"] == 100.0
    assert metrics["coverage"]["symbol_line_avg_percent"] == 90.0
    assert metrics["cost"]["avg_tokens_per_symbol"] == 75.0
    assert metrics["performance"]["avg_duration_seconds_per_symbol"] == 1.3
    assert metrics["productivity"]["valid_tests_saved_per_llm_call"] == 0.5


def test_format_suite_metrics_table_contains_headers() -> None:
    text = format_suite_metrics_table({
        "symbols_processed": 1,
        "symbols_executable": 1,
        "symbols_saved": 1,
        "rates": {
            "valid_generation_percent": 100.0,
            "approval_percent": 100.0,
            "first_attempt_success_percent": 100.0,
        },
        "coverage": {
            "symbol_line_avg_percent": 80.0,
            "symbol_branch_avg_percent": 50.0,
            "repository_line_avg_percent": 80.0,
            "module_line_avg_percent": {},
        },
        "cost": {"avg_tokens_per_symbol": 10, "avg_cost_usd_per_symbol": 0.01},
        "performance": {"avg_duration_seconds_per_symbol": 1.2},
        "productivity": {"valid_tests_saved_per_llm_call": 1.0},
    })
    assert "Taxa de geração válida" in text
    assert "Sucesso na 1ª geração" in text
    assert "100.0%" in text
