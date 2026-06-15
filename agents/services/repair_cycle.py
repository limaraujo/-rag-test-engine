from __future__ import annotations

import logging

from agents.policies.llm_budget import LLMBudget, error_fingerprint
from agents.repair import RepairAgent
from execution.runner import RunResult, TestRunner
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from schemas.pipeline import SymbolRunRecord, SymbolState

logger = logging.getLogger(__name__)


def run_repair_loop(
    ctx: FunctionContext,
    test: GeneratedTest,
    result: RunResult,
    pythonpath: list[str],
    budget: LLMBudget,
    record: SymbolRunRecord,
    *,
    repair_agent: RepairAgent,
    runner: TestRunner,
    max_repairs: int,
) -> tuple[GeneratedTest, RunResult, bool, LLMBudget, SymbolRunRecord]:
    repaired = False
    last_error_fp: str | None = None

    for attempt in range(1, max_repairs + 1):
        if result.passed:
            record.set_state(SymbolState.PASSED)
            break

        error_fp = error_fingerprint(result)
        if error_fp == last_error_fp:
            record.stop_reason = "same_error_repeated"
            logger.info("  [repair] mesmo erro repetido — parando")
            break
        last_error_fp = error_fp

        if not budget.can_call():
            record.stop_reason = "llm_budget_exhausted"
            logger.warning(
                "  [repair] orçamento LLM esgotado (%d/%d)",
                budget.calls,
                budget.max_calls,
            )
            break

        logger.info("  [repair] tentativa %d/%d …", attempt, max_repairs)
        record.set_state(SymbolState.REPAIRING)
        try:
            if not budget.record(f"repair_{attempt}"):
                record.stop_reason = "llm_budget_exhausted"
                break
            test = repair_agent.repair(ctx, test, result, attempt=attempt)
            result = runner.run(test, pythonpath=pythonpath)
            if result.passed:
                repaired = True
                record.set_state(SymbolState.PASSED)
        except Exception as exc:
            record.stop_reason = f"repair_error:{exc}"
            logger.warning("  [repair] erro: %s", exc)
            break

    if not result.passed and not record.stop_reason:
        record.set_state(SymbolState.TEST_FAILED)
    return test, result, repaired, budget, record
