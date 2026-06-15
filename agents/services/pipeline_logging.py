from __future__ import annotations

import logging
from pathlib import Path

from config.run_workspace import RunWorkspace
from config.settings import settings
from execution.runner import RunResult, SuiteValidationResult
from parsers.source.path_filters import ScanResult
from parsers.source.symbol_filter import SymbolFilterResult, SymbolFilterStats
from schemas.pipeline import PipelineStats, SymbolRunRecord

logger = logging.getLogger(__name__)


def log_ingest_selection(
    source_dir: Path,
    scan_result: ScanResult,
    filter_result: SymbolFilterResult,
    *,
    selection_artifact: Path | None = None,
) -> None:
    """Registra no log quais arquivos e símbolos entraram ou ficaram de fora."""
    root = source_dir.resolve()

    logger.info(
        "[ingest] arquivos: %d incluído(s), %d ignorado(s)",
        scan_result.included,
        scan_result.excluded,
    )
    for path in scan_result.files:
        rel = path.resolve().relative_to(root).as_posix()
        logger.info("  [arquivo +] %s", rel)
    for item in scan_result.excluded_files:
        logger.info("  [arquivo -] %s (%s)", item.path, item.reason)

    logger.info(
        "[ingest] símbolos: %d elegíveis para testes, %d filtrados",
        len(filter_result.kept),
        filter_result.stats.filtered_total,
    )
    for symbol in filter_result.kept:
        logger.info(
            "  [símbolo +] %s (%s)",
            symbol.qualified_name,
            symbol.symbol_type,
        )
    for item in filter_result.filtered:
        logger.info(
            "  [símbolo -] %s (%s) — %s",
            item.qualified_name,
            item.symbol_type,
            item.reason,
        )

    if selection_artifact is not None:
        logger.info("[ingest] seleção completa em %s", selection_artifact)


def log_pytest_result(result: RunResult, *, label: str = "pytest") -> None:
    if result.passed:
        logger.info(
            "  [%s] ok — %d passaram em %.2fs",
            label,
            result.num_passed,
            result.duration_seconds,
        )
    else:
        logger.warning(
            "  [%s] falhou — %d passaram, %d falharam, %d erros (exit %d)",
            label,
            result.num_passed,
            result.num_failed,
            result.num_errors,
            result.exit_code,
        )


def log_coverage_summary(summary: dict, record: SymbolRunRecord) -> None:
    line_pct = summary.get("line_coverage_percent")
    branch_pct = summary.get("branch_coverage_percent")
    threshold = summary.get("threshold_percent")
    uncovered_branches = summary.get("uncovered_branches") or []
    branch_note = (
        f", branches={branch_pct}% ({len(uncovered_branches)} não cobertos)"
        if branch_pct is not None
        else ""
    )
    if record.previous_coverage_percent is not None:
        logger.info(
            "  [coverage] linhas=%s%% (antes=%s%%, threshold=%s%%)%s",
            line_pct,
            record.previous_coverage_percent,
            threshold,
            branch_note,
        )
    else:
        logger.info(
            "  [coverage] linhas=%s%% (threshold=%s%%)%s",
            line_pct,
            threshold,
            branch_note,
        )


def validation_payload(validation: SuiteValidationResult) -> dict:
    return {
        "passed": validation.passed,
        "exit_code": validation.exit_code,
        "tests_dir": validation.tests_dir,
        "num_passed": validation.num_passed,
        "num_failed": validation.num_failed,
        "num_errors": validation.num_errors,
        "duration_seconds": validation.duration_seconds,
    }


def collect_ignored_symbols(
    filter_stats: SymbolFilterStats,
    stats: PipelineStats,
) -> list[dict]:
    ignored: list[dict] = []
    if filter_stats.filtered_total:
        ignored.append({
            "scope": "ingest_filter",
            "count": filter_stats.filtered_total,
            "reason": "filtered_before_generation",
            "detail": filter_stats.to_dict(),
        })
    for record in stats.symbol_runs:
        if not record.stop_reason:
            continue
        ignored.append({
            "qualified_name": record.qualified_name,
            "reason": record.stop_reason,
            "state": record.state.value,
            "from_cache": record.from_cache,
        })
    return ignored


def log_run_summary(
    workspace: RunWorkspace,
    stats: PipelineStats,
    token_summary: str | None,
    *,
    validation: SuiteValidationResult | None = None,
    filter_stats: SymbolFilterStats | None = None,
) -> None:
    logger.info("")
    logger.info("=" * 52)
    if filter_stats is not None:
        logger.info(
            "  Símbolos extraídos   : %d",
            filter_stats.extracted_total,
        )
        logger.info(
            "  Filtrados (sem teste): %d (%d container_class)",
            filter_stats.filtered_total,
            filter_stats.removed_container_class,
        )
    logger.info("  Símbolos processados : %d", stats.total)
    logger.info(
        "  Testes salvos        : %d (%d após reparo, %d com boost de cobertura)",
        stats.ok,
        stats.repaired,
        stats.coverage_boosted,
    )
    logger.info("  Falharam (descartados): %d", stats.failed)
    logger.info("  Ignorados (erros)    : %d", stats.skipped)
    gc = stats.generation_cache
    logger.info(
        "  Cache de geração     : %d hits, %d misses, %d stale, "
        "%d invalidações, %d LLM evitadas",
        gc.hits,
        gc.misses,
        gc.stale,
        gc.invalidations,
        gc.llm_calls_avoided,
    )
    logger.info("  Workspace            : %s", workspace.root)
    logger.info("  Testes               : %s", workspace.tests_dir)
    logger.info("  Artefatos            : %s", workspace.artifacts_dir)
    if validation is not None:
        status = "ok" if validation.passed else "FALHOU"
        logger.info(
            "  Validação pytest     : %s (%d passaram, %d falharam)",
            status,
            validation.num_passed,
            validation.num_failed,
        )
    measured = [
        r for r in stats.symbol_runs
        if r.current_coverage_percent is not None
    ]
    if measured:
        avg_line = round(
            sum(r.current_coverage_percent or 0 for r in measured) / len(measured),
            1,
        )
        branch_values = [
            r.current_branch_coverage_percent
            for r in measured
            if r.current_branch_coverage_percent is not None
        ]
        if branch_values:
            avg_branch = round(sum(branch_values) / len(branch_values), 1)
            logger.info(
                "  Cobertura média      : linhas=%s%%, branches=%s%% (%d símbolos)",
                avg_line,
                avg_branch,
                len(measured),
            )
        else:
            logger.info(
                "  Cobertura média      : linhas=%s%% (%d símbolos)",
                avg_line,
                len(measured),
            )
    if token_summary:
        logger.info("  Uso de tokens (OpenAI)")
        for line in token_summary.splitlines():
            logger.info(line)
    if settings.LOG_API_CALLS:
        logger.info("  Chamadas API         : %s", workspace.logs_dir / "api_calls")
    logger.info("=" * 52)
