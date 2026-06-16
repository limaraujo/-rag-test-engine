from __future__ import annotations

import logging

from agents.policies.llm_budget import LLMBudget
from agents.services.pipeline_logging import log_coverage_summary, log_pytest_result
from agents.services.repair_cycle import run_repair_loop
from agents.repair import RepairAgent
from agents.test_generator import TestGeneratorAgent
from config.settings import settings
from execution.coverage_analyzer import CoverageAnalyzer, coverage_round_signature
from execution.runner import RunResult, TestRunner
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from schemas.pipeline import SymbolRunRecord, SymbolState

logger = logging.getLogger(__name__)


def measure_coverage(
    ctx: FunctionContext,
    test: GeneratedTest,
    pythonpath: list[str],
    record: SymbolRunRecord,
) -> dict:
    record.set_state(SymbolState.COVERAGE_CHECKED)
    analyzer = CoverageAnalyzer(
        test,
        ctx.file_path,
        target_function=ctx.qualified_name,
        pythonpath=pythonpath,
        threshold=settings.COVERAGE_THRESHOLD,
    )
    cov_result = analyzer.run()
    record.record_pytest_result(cov_result)
    summary = analyzer.generate_summary()
    record.record_coverage_summary(summary)
    log_coverage_summary(summary, record)
    if not cov_result.passed:
        logger.warning(
            "  [coverage] pytest falhou durante medição (exit %d)",
            cov_result.exit_code,
        )
    return summary


def run_coverage_loop(
    ctx: FunctionContext,
    test: GeneratedTest,
    result: RunResult,
    pythonpath: list[str],
    budget: LLMBudget,
    record: SymbolRunRecord,
    *,
    repaired: bool,
    generator: TestGeneratorAgent,
    runner: TestRunner,
    repair_agent: RepairAgent,
    max_repairs: int,
) -> tuple[GeneratedTest, RunResult, bool, bool, LLMBudget, SymbolRunRecord]:
    coverage_boosted = False
    approved_test = test
    approved_result = result

    summary = measure_coverage(ctx, approved_test, pythonpath, record)
    if summary.get("meets_threshold") or settings.MAX_COVERAGE_ROUNDS <= 0:
        return approved_test, approved_result, repaired, coverage_boosted, budget, record

    seen_signatures: set[str] = set()
    last_pct_before_regen: float | None = summary.get("line_coverage_percent")

    for cov_round in range(1, settings.MAX_COVERAGE_ROUNDS + 1):
        if not budget.can_call():
            record.stop_reason = record.stop_reason or "llm_budget_exhausted"
            logger.warning(
                "  [coverage] orçamento LLM esgotado — mantendo teste aprovado",
            )
            break

        current_pct = summary.get("line_coverage_percent")
        logger.info(
            "  [coverage] %s%% < %s%% — regenerando (%d/%d) …",
            current_pct,
            summary.get("threshold_percent"),
            cov_round,
            settings.MAX_COVERAGE_ROUNDS,
        )

        ctx = ctx.model_copy(update={
            "coverage_gaps": summary.get("gaps") or [],
            "coverage_summary": summary,
        })
        try:
            if not budget.record(f"coverage_{cov_round}"):
                record.stop_reason = record.stop_reason or "llm_budget_exhausted"
                break
            candidate = generator.generate(ctx, operation=f"coverage_{cov_round}")
        except Exception as exc:
            record.stop_reason = record.stop_reason or f"coverage_error:{exc}"
            logger.warning("  [coverage] erro na regeneração: %s", exc)
            break

        candidate_result = runner.run(candidate, pythonpath=pythonpath)
        record.record_pytest_result(candidate_result)
        log_pytest_result(candidate_result, label="coverage")
        if not candidate_result.passed:
            candidate, candidate_result, post_repair, budget, record = run_repair_loop(
                ctx,
                candidate,
                candidate_result,
                pythonpath,
                budget,
                record,
                repair_agent=repair_agent,
                runner=runner,
                max_repairs=max_repairs,
            )
            repaired = repaired or post_repair
            if not candidate_result.passed:
                logger.warning(
                    "  [coverage] regeneração falhou — mantendo teste aprovado anterior",
                )
                break

        approved_test = candidate
        approved_result = candidate_result
        coverage_boosted = True

        summary = measure_coverage(ctx, approved_test, pythonpath, record)
        if summary.get("meets_threshold"):
            logger.info("  [coverage] threshold atingido — parando")
            break

        round_sig = coverage_round_signature(summary)
        if round_sig in seen_signatures:
            record.set_state(SymbolState.COVERAGE_STALLED)
            record.stop_reason = record.stop_reason or "identical_coverage_round"
            logger.info("  [coverage] rodada idêntica — parando")
            break
        seen_signatures.add(round_sig)

        new_pct = summary.get("line_coverage_percent")
        if (
            settings.COVERAGE_STOP_ON_NO_IMPROVEMENT
            and last_pct_before_regen is not None
            and new_pct is not None
            and new_pct <= last_pct_before_regen
        ):
            record.set_state(SymbolState.COVERAGE_STALLED)
            record.stop_reason = record.stop_reason or "coverage_no_improvement"
            logger.info("  [coverage] sem melhoria — parando")
            break
        last_pct_before_regen = new_pct

    return approved_test, approved_result, repaired, coverage_boosted, budget, record
