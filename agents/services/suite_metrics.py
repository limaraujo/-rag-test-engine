"""Métricas de qualidade da suíte gerada (referência inicial 0% — sem antes/depois)."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from execution.runner import RunResult, SuiteValidationResult
from parsers.source.symbol_filter import SymbolFilterStats
from schemas.pipeline import PipelineStats, SymbolRunRecord


def is_suite_executable(
    result: RunResult | None,
    *,
    skipped: bool = False,
    stop_reason: str | None = None,
) -> bool:
    """
    Suíte executável: pytest coletou e rodou testes sem erro estrutural.

    Inválida: sintaxe, import, fixture, coleta (exit 2), exceção no pipeline.
    """
    if skipped:
        return False
    if stop_reason and stop_reason.startswith("error:"):
        return False
    if result is None:
        return False
    if result.exit_code == 2:
        return False
    collected = result.num_passed + result.num_failed
    if result.num_errors > 0 and collected == 0:
        return False
    return collected > 0 or result.passed


def tests_collected_count(result: RunResult | None) -> int:
    if result is None:
        return 0
    return result.num_passed + result.num_failed


def _pct(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(100.0 * numerator / denominator, 1)


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 1)


def _coverage_by_module(records: list[SymbolRunRecord]) -> dict[str, float]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for record in records:
        if record.current_coverage_percent is None or not record.file_path:
            continue
        module_key = Path(record.file_path).parent.as_posix() or "."
        buckets[module_key].append(record.current_coverage_percent)
    return {key: _mean(vals) or 0.0 for key, vals in sorted(buckets.items())}


def build_suite_metrics(
    stats: PipelineStats,
    *,
    filter_stats: SymbolFilterStats | None = None,
    token_usage: dict[str, Any] | None = None,
    validation: SuiteValidationResult | None = None,
) -> dict[str, Any]:
    """Calcula métricas agregadas da execução."""
    runs = stats.symbol_runs
    symbols_processed = len(runs)

    executable = [r for r in runs if r.suite_executable]
    symbols_executable = len(executable)

    first_attempt_ok = sum(
        1
        for r in runs
        if r.suite_executable and r.first_generation_passed and not r.from_cache
    )

    valid_generation_rate = _pct(symbols_executable, symbols_processed)

    tests_collected = sum(r.tests_collected for r in runs if r.suite_executable)
    if validation is not None and validation.num_passed + validation.num_failed > 0:
        tests_approved = validation.num_passed
        tests_denominator = validation.num_passed + validation.num_failed
    else:
        tests_approved = sum(r.pytest_num_passed or 0 for r in runs if r.passed)
        tests_denominator = tests_collected
    approval_rate = _pct(tests_approved, tests_denominator)

    first_attempt_success_rate = _pct(first_attempt_ok, symbols_processed)

    measured = [r for r in runs if r.current_coverage_percent is not None]
    line_values = [r.current_coverage_percent for r in measured if r.current_coverage_percent is not None]
    branch_values = [
        r.current_branch_coverage_percent
        for r in measured
        if r.current_branch_coverage_percent is not None
    ]
    symbol_line_avg = _mean(line_values)
    symbol_branch_avg = _mean(branch_values)
    module_coverage = _coverage_by_module(measured)
    repository_line_avg = symbol_line_avg

    total_llm_calls = sum(r.llm_calls for r in runs)
    valid_tests_per_call = (
        round(stats.ok / total_llm_calls, 2) if total_llm_calls > 0 else None
    )

    durations = [r.duration_seconds for r in runs if r.duration_seconds > 0]
    avg_duration = round(sum(durations) / len(durations), 2) if durations else 0.0
    total_duration = round(sum(durations), 2)

    by_symbol_usage = (token_usage or {}).get("by_symbol") or {}
    processed_names = {r.qualified_name for r in runs}
    symbol_token_total = sum(
        int(by_symbol_usage.get(name, {}).get("total_tokens", 0) or 0)
        for name in processed_names
    )
    symbol_cost_total = sum(
        float(by_symbol_usage.get(name, {}).get("estimated_cost", 0) or 0)
        for name in processed_names
        if by_symbol_usage.get(name, {}).get("estimated_cost") is not None
    )
    has_cost = any(
        by_symbol_usage.get(name, {}).get("estimated_cost") is not None
        for name in processed_names
    )

    avg_tokens_per_symbol = (
        round(symbol_token_total / symbols_processed, 1)
        if symbols_processed and symbol_token_total
        else None
    )
    avg_cost_per_symbol = (
        round(symbol_cost_total / symbols_processed, 6)
        if symbols_processed and has_cost
        else None
    )

    per_symbol = []
    for record in runs:
        usage = by_symbol_usage.get(record.qualified_name, {})
        per_symbol.append({
            "qualified_name": record.qualified_name,
            "file_path": record.file_path,
            "suite_executable": record.suite_executable,
            "first_generation_passed": record.first_generation_passed,
            "passed": record.passed,
            "repaired": record.repaired,
            "from_cache": record.from_cache,
            "tests_collected": record.tests_collected,
            "pytest_num_passed": record.pytest_num_passed,
            "pytest_num_failed": record.pytest_num_failed,
            "pytest_num_errors": record.pytest_num_errors,
            "line_coverage_percent": record.current_coverage_percent,
            "branch_coverage_percent": record.current_branch_coverage_percent,
            "llm_calls": record.llm_calls,
            "duration_seconds": record.duration_seconds,
            "total_tokens": usage.get("total_tokens"),
            "estimated_cost": usage.get("estimated_cost"),
            "stop_reason": record.stop_reason,
        })

    return {
        "reference_baseline_percent": 0.0,
        "symbols_eligible": (
            filter_stats.extracted_total - filter_stats.filtered_total
            if filter_stats
            else None
        ),
        "symbols_processed": symbols_processed,
        "symbols_executable": symbols_executable,
        "symbols_saved": stats.ok,
        "symbols_failed": stats.failed,
        "symbols_skipped": stats.skipped,
        "rates": {
            "valid_generation_percent": valid_generation_rate,
            "approval_percent": approval_rate,
            "first_attempt_success_percent": first_attempt_success_rate,
        },
        "tests": {
            "collected": tests_collected,
            "approved": tests_approved,
            "denominator_for_approval_rate": tests_denominator,
        },
        "coverage": {
            "symbol_line_avg_percent": symbol_line_avg,
            "symbol_branch_avg_percent": symbol_branch_avg,
            "module_line_avg_percent": module_coverage,
            "repository_line_avg_percent": repository_line_avg,
            "symbols_measured": len(measured),
            "note": (
                "Cobertura de repositório/módulo é média dos símbolos já processados "
                "(referência inicial 0%; suíte criada do zero)."
            ),
        },
        "cost": {
            "total_llm_calls": total_llm_calls,
            "total_tokens": symbol_token_total or None,
            "total_estimated_cost_usd": round(symbol_cost_total, 6) if has_cost else None,
            "avg_tokens_per_symbol": avg_tokens_per_symbol,
            "avg_cost_usd_per_symbol": avg_cost_per_symbol,
        },
        "performance": {
            "total_duration_seconds": total_duration,
            "avg_duration_seconds_per_symbol": avg_duration,
        },
        "productivity": {
            "valid_tests_saved_per_llm_call": valid_tests_per_call,
        },
        "per_symbol": per_symbol,
    }


def format_suite_metrics_table(metrics: dict[str, Any]) -> str:
    """Formata tabela legível para logs."""
    rates = metrics.get("rates") or {}
    coverage = metrics.get("coverage") or {}
    cost = metrics.get("cost") or {}
    perf = metrics.get("performance") or {}
    productivity = metrics.get("productivity") or {}

    def _fmt_pct(value: float | None) -> str:
        return f"{value:.1f}%" if value is not None else "n/d"

    def _fmt_num(value: float | int | None, *, suffix: str = "") -> str:
        if value is None:
            return "n/d"
        if isinstance(value, float) and value == int(value):
            return f"{int(value)}{suffix}"
        return f"{value}{suffix}"

    rows = [
        ("Dimensão", "Métrica", "Valor"),
        ("Validade", "Taxa de geração válida", _fmt_pct(rates.get("valid_generation_percent"))),
        ("Correção", "Taxa de aprovação", _fmt_pct(rates.get("approval_percent"))),
        ("Cobertura", "Linhas (média símbolo-alvo)", _fmt_pct(coverage.get("symbol_line_avg_percent"))),
        ("Cobertura", "Branches (média símbolo-alvo)", _fmt_pct(coverage.get("symbol_branch_avg_percent"))),
        ("Cobertura", "Linhas (média repositório parcial)", _fmt_pct(coverage.get("repository_line_avg_percent"))),
        ("Autonomia", "Sucesso na 1ª geração", _fmt_pct(rates.get("first_attempt_success_percent"))),
        ("Custo", "Tokens médios / símbolo", _fmt_num(cost.get("avg_tokens_per_symbol"))),
        ("Custo", "USD médios / símbolo", _fmt_num(cost.get("avg_cost_usd_per_symbol"))),
        ("Desempenho", "Tempo médio / símbolo", _fmt_num(perf.get("avg_duration_seconds_per_symbol"), suffix="s")),
        ("Produtividade", "Testes salvos / chamada LLM", _fmt_num(productivity.get("valid_tests_saved_per_llm_call"))),
    ]

    col_widths = [
        max(len(row[i]) for row in rows) for i in range(3)
    ]
    lines: list[str] = []
    for index, row in enumerate(rows):
        line = "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row))
        lines.append(line)
        if index == 0:
            lines.append("  ".join("-" * col_widths[i] for i in range(3)))
    lines.append("")
    lines.append(
        f"  Símbolos: {metrics.get('symbols_processed', 0)} processados, "
        f"{metrics.get('symbols_executable', 0)} executáveis, "
        f"{metrics.get('symbols_saved', 0)} salvos"
    )
    module_cov = coverage.get("module_line_avg_percent") or {}
    if module_cov:
        lines.append("  Cobertura por módulo (linhas, média símbolos medidos):")
        for module, pct in module_cov.items():
            lines.append(f"    {module}: {pct:.1f}%")
    return "\n".join(lines)
