from __future__ import annotations

import logging

from agents.policies.llm_budget import LLMBudget, LLMBudgetExhausted
from agents.test_generator import TestGeneratorAgent
from cache.generation_cache import GenerationCache
from config.run_workspace import RunWorkspace
from execution.pytest_support import safe_test_stem
from execution.runner import RunResult, TestRunner
from retrieval.retriever import Retriever
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from schemas.pipeline import GenerationCacheStats, PipelineStats

logger = logging.getLogger(__name__)


def generate_with_cache(
    ctx: FunctionContext,
    *,
    pythonpath: list[str],
    cache_stats: GenerationCacheStats,
    budget: LLMBudget,
    generator: TestGeneratorAgent,
    runner: TestRunner,
    generation_cache: GenerationCache,
) -> tuple[GeneratedTest, bool, RunResult | None]:
    operation = "generate"
    model = generator.model_name
    cache = generation_cache

    def _generate() -> GeneratedTest:
        if not budget.record("generate"):
            raise LLMBudgetExhausted("generate")
        return generator.generate(ctx, operation=operation)

    if not cache.enabled:
        cache_stats.misses += 1
        return _generate(), False, None

    cache_key = cache.build_cache_key(ctx, operation=operation, model=model)
    path = cache._entry_path(cache_key)
    entry = cache.lookup(ctx, operation=operation, model=model)

    if entry is None:
        if path.is_file():
            raw = cache._read_json(path)
            if raw is None:
                cache_stats.invalidations += 1
            elif raw.get("status") == "stale":
                pass
            else:
                cache_stats.invalidations += 1
        cache_stats.misses += 1
        logger.info("  [cache miss] %s", ctx.qualified_name)
        return _generate(), False, None

    test = cache.materialize(entry)
    result = runner.run(test, pythonpath=pythonpath)
    if result.passed:
        cache_stats.hits += 1
        cache_stats.llm_calls_avoided += 1
        logger.info("  [cache hit] %s", ctx.qualified_name)
        return test, True, result

    cache.mark_stale(entry.cache_key, reason="pytest_failed")
    cache_stats.stale += 1
    cache_stats.misses += 1
    logger.info("  [cache stale] %s — regenerando", ctx.qualified_name)
    try:
        return _generate(), False, None
    except LLMBudgetExhausted:
        logger.warning(
            "  [cache stale] orçamento LLM esgotado — mantendo teste falho",
        )
        return test, False, result


def save_approved_test(
    workspace: RunWorkspace,
    qname: str,
    test: GeneratedTest,
    result: RunResult,
    repaired: bool,
    coverage_boosted: bool,
    stats: PipelineStats,
    *,
    ctx: FunctionContext | None = None,
    generator: TestGeneratorAgent | None = None,
    generation_cache: GenerationCache | None = None,
    retriever: Retriever | None = None,
) -> None:
    dest = workspace.tests_dir / f"test_{safe_test_stem(qname)}.py"
    dest.write_text(test.full_code, encoding="utf-8")

    label = " (reparado)" if repaired else ""
    cov_label = " +cobertura" if coverage_boosted else ""
    logger.info(
        "  [ok%s%s] %d testes → %s",
        label,
        cov_label,
        result.num_passed,
        dest.name,
    )
    stats.ok += 1
    if repaired:
        stats.repaired += 1
    if coverage_boosted:
        stats.coverage_boosted += 1

    if (
        ctx is not None
        and generator is not None
        and generation_cache is not None
        and generation_cache.enabled
    ):
        generation_cache.save(
            ctx,
            test,
            operation="generate",
            model=generator.model_name,
            coverage=ctx.coverage_summary,
        )
        if retriever is not None:
            try:
                retriever.index_generated_test(ctx.qualified_name, test.full_code)
            except Exception as exc:
                logger.warning("  [index_tests] %s", exc)
