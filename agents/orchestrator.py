from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from agents.repair import RepairAgent
from agents.test_generator import TestGeneratorAgent
from cache.generation_cache import GenerationCache
from config.logging_setup import setup_logging
from config.run_workspace import RunWorkspace, save_ingest_artifacts, save_run_summary
from config.settings import ROOT, settings
from execution.coverage_analyzer import CoverageAnalyzer, coverage_round_signature
from execution.runner import RunResult, SuiteValidationResult, TestRunner
from ingest.call_graph import CallGraph
from ingest.dependency_graph import DependencyGraph
from ingest.models.ExtractedSymbol import ExtractedSymbol
from ingest.symbol_filter import SymbolFilterStats, filter_symbols
from ingest.path_filters import emit_scan_warnings, scan_python_files
from ingest.parser import parse_repository_graphs
from llm.call_logger import setup_api_call_logging
from llm.usage_tracker import get_tracker, reset_tracker
from retrieval.retriever import Retriever
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from schemas.pipeline import (
    GenerationCacheStats,
    OrchestrationResult,
    PipelineStats,
    SymbolRunRecord,
    SymbolState,
)
logger = logging.getLogger(__name__)


class LLMBudgetExhausted(RuntimeError):
    """Orçamento de chamadas LLM por símbolo esgotado."""


@dataclass
class _LLMBudget:
    max_calls: int
    calls: int = 0
    operations: list[str] = field(default_factory=list)

    def can_call(self) -> bool:
        return self.calls < self.max_calls

    def record(self, operation: str) -> bool:
        if not self.can_call():
            return False
        self.calls += 1
        self.operations.append(operation)
        return True


def _error_fingerprint(result: RunResult) -> str:
    text = (result.failure_summary or result.output).strip()
    text = re.sub(r"C:\\Users\\[^\s]+|/tmp[^\s]+|/var/folders/[^\s]+", "<tmp>", text)
    text = re.sub(r"\d+\.\d+s\b", "<dur>", text)
    key_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("E ", ">", "assert ")):
            key_lines.append(stripped)
        elif any(token in stripped for token in ("Error", "AssertionError", "FAILED")):
            key_lines.append(stripped)
    if key_lines:
        text = "\n".join(key_lines)
    if len(text) > settings.REPAIR_ERROR_MAX_CHARS:
        text = text[: settings.REPAIR_ERROR_MAX_CHARS]
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class OrchestratorAgent:
    """
    Orquestra o pipeline completo de geração de testes com RAG.

    Fases:
        1. Ingestão  — parser + grafos + artefatos
        2. Indexação — embeddings no Qdrant
        3. Geração   — LLM + RAG por símbolo
        4. Execução  — pytest
        5. Reparo    — LLM corrige falhas
        6. Cobertura — regenera se abaixo do threshold
        7. Salvamento — tests/ + run_summary.json
        8. Validação  — pytest na pasta tests/ completa
    """

    def __init__(
        self,
        *,
        retriever: Retriever | None = None,
        generator: TestGeneratorAgent | None = None,
        runner: TestRunner | None = None,
        repair_agent: RepairAgent | None = None,
        max_repairs: int | None = None,
        generation_cache: GenerationCache | None = None,
    ) -> None:
        self._retriever = retriever or Retriever()
        self._generator = generator or TestGeneratorAgent()
        self._runner = runner or TestRunner()
        self._repair_agent = repair_agent or RepairAgent()
        self._max_repairs = max_repairs if max_repairs is not None else settings.MAX_REPAIRS
        self._generation_cache = generation_cache or GenerationCache()

    def run(self, source_dir: str | Path = ".") -> OrchestrationResult:
        src = Path(source_dir).resolve()
        workspace = RunWorkspace.create(src)

        log_file = setup_logging(workspace.logs_dir / "pipeline.log")
        logger.info("Workspace: %s", workspace.root)
        logger.info("Log: %s", log_file)

        api_calls_dir = workspace.logs_dir / "api_calls"
        active_calls_dir = setup_api_call_logging(api_calls_dir)
        if active_calls_dir:
            logger.info("API calls log: %s", active_calls_dir)

        if settings.AI_MODE == "offline":
            logger.warning("AI_MODE=offline — embeddings e LLM locais (sem API OpenAI)")

        reset_tracker()

        all_symbols, test_symbols, call_graph, dependency_graph, filter_stats = (
            self._ingest(src, workspace)
        )
        indexed, cache_hits = self._index(all_symbols)
        stats = self._process_symbols(
            test_symbols,
            workspace=workspace,
            call_graph=call_graph,
            dependency_graph=dependency_graph,
            source_dir=src,
            all_symbols=all_symbols,
        )

        validation = self._validate_suite(workspace)

        token_summary = None
        if settings.AI_MODE != "offline":
            token_summary = get_tracker().format_summary()

        save_run_summary(
            workspace,
            stats={
                "ok": stats.ok,
                "repaired": stats.repaired,
                "failed": stats.failed,
                "skipped": stats.skipped,
                "coverage_boosted": stats.coverage_boosted,
                "symbol_filter": filter_stats.to_dict(),
                "generation_cache": stats.generation_cache.to_dict(),
                "symbol_runs": [record.to_dict() for record in stats.symbol_runs],
            },
            token_summary=token_summary,
            validation=self._validation_payload(validation),
        )
        self._log_summary(workspace, stats, token_summary, validation, filter_stats)

        return OrchestrationResult(
            workspace=workspace,
            stats=stats,
            indexed=indexed,
            cache_hits=cache_hits,
            token_summary=token_summary,
            validation=validation,
            generation_cache=stats.generation_cache,
        )

    def _ingest(
        self,
        src: Path,
        workspace: RunWorkspace,
    ) -> tuple[
        list[ExtractedSymbol],
        list[ExtractedSymbol],
        CallGraph,
        DependencyGraph,
        SymbolFilterStats,
    ]:
        logger.info("[ingest] scanning %s …", src)
        scan_result = scan_python_files(src)
        emit_scan_warnings(src, scan_result)
        all_symbols, call_graph, dependency_graph = parse_repository_graphs(str(src))
        logger.info("[ingest] %d symbols found", len(all_symbols))
        logger.info(
            "[ingest] call graph: %d nodes, dependency graph: %d nodes",
            len(call_graph.nodes),
            len(dependency_graph.nodes),
        )

        save_ingest_artifacts(
            workspace,
            symbols=all_symbols,
            call_graph=call_graph,
            dependency_graph=dependency_graph,
        )
        logger.info("[ingest] artefatos salvos em %s", workspace.artifacts_dir)

        filter_result = filter_symbols(all_symbols)
        test_symbols = filter_result.kept
        filter_stats = filter_result.stats
        if filter_stats.filtered_total:
            logger.info(
                "[ingest] %d símbolo(s) filtrado(s) para geração "
                "(%d container_class, %d elegíveis)",
                filter_stats.filtered_total,
                filter_stats.removed_container_class,
                len(test_symbols),
            )

        return all_symbols, test_symbols, call_graph, dependency_graph, filter_stats

    def _index(self, symbols: list[ExtractedSymbol]) -> tuple[int, int]:
        if settings.REINDEX_SYMBOLS:
            logger.info("[index] reindexando todos os símbolos no Qdrant …")
        else:
            logger.info("[index] indexação incremental (REINDEX_SYMBOLS=false) …")

        indexed, cache_hits = self._retriever.index_symbols(symbols)
        logger.info("[index] %d indexados, %d reutilizados do cache", indexed, cache_hits)
        return indexed, cache_hits

    def _process_symbols(
        self,
        symbols: list[ExtractedSymbol],
        *,
        workspace: RunWorkspace,
        call_graph: CallGraph,
        dependency_graph: DependencyGraph,
        source_dir: Path,
        all_symbols: list[ExtractedSymbol],
    ) -> PipelineStats:
        stats = PipelineStats()
        symbols_by_name = {symbol.qualified_name: symbol for symbol in all_symbols}
        pythonpath = [str(ROOT)]

        for symbol in symbols:
            self._process_symbol(
                symbol,
                workspace=workspace,
                call_graph=call_graph,
                dependency_graph=dependency_graph,
                symbols_by_name=symbols_by_name,
                source_dir=source_dir,
                pythonpath=pythonpath,
                stats=stats,
            )

        return stats

    def _process_symbol(
        self,
        symbol: ExtractedSymbol,
        *,
        workspace: RunWorkspace,
        call_graph: CallGraph,
        dependency_graph: DependencyGraph,
        symbols_by_name: dict[str, ExtractedSymbol],
        source_dir: Path,
        pythonpath: list[str],
        stats: PipelineStats,
    ) -> None:
        qname = symbol.qualified_name
        record = SymbolRunRecord(qualified_name=qname)
        budget = _LLMBudget(settings.MAX_LLM_CALLS_PER_SYMBOL)
        logger.info("[gen] %s", qname)

        ctx = FunctionContext.from_symbol(symbol, project_root=ROOT)
        ctx = self._retriever.enrich(
            ctx,
            symbol,
            call_graph=call_graph,
            dependency_graph=dependency_graph,
            symbols_by_name=symbols_by_name,
            project_root=source_dir,
        )

        try:
            try:
                test, from_cache, cached_result = self._generate_with_cache(
                    ctx,
                    pythonpath=pythonpath,
                    cache_stats=stats.generation_cache,
                    budget=budget,
                )
            except LLMBudgetExhausted:
                record.stop_reason = "llm_budget_exhausted"
                stats.failed += 1
                return
            record.from_cache = from_cache
            repaired = False

            if from_cache and cached_result is not None:
                result = cached_result
                if result.passed:
                    record.set_state(SymbolState.PASSED)
                else:
                    record.set_state(SymbolState.TEST_FAILED)
            else:
                record.set_state(SymbolState.GENERATED)
                result = self._runner.run(test, pythonpath=pythonpath)
                if result.passed:
                    record.set_state(SymbolState.PASSED)
                else:
                    record.set_state(SymbolState.TEST_FAILED)
                    test, result, repaired, budget, record = self._repair_loop(
                        ctx, test, result, pythonpath, budget, record,
                    )

            coverage_boosted = False
            if result.passed:
                test, result, repaired, coverage_boosted, budget, record = (
                    self._coverage_loop(
                        ctx,
                        test,
                        result,
                        pythonpath,
                        repaired=repaired,
                        budget=budget,
                        record=record,
                    )
                )

            record.passed = result.passed
            record.repaired = repaired
            record.coverage_boosted = coverage_boosted
            record.llm_calls = budget.calls

            if result.passed:
                self._save_test(
                    workspace,
                    qname,
                    test,
                    result,
                    repaired,
                    coverage_boosted,
                    stats,
                    ctx=ctx,
                )
            else:
                if not record.stop_reason:
                    record.stop_reason = "tests_failed"
                logger.warning(
                    "  [fail] %d falharam, %d erros — ignorando (%s)",
                    result.num_failed,
                    result.num_errors,
                    record.stop_reason or record.state.value,
                )
                stats.failed += 1
        except Exception as exc:
            record.stop_reason = f"error:{exc}"
            logger.warning("  [skip] erro no símbolo %s: %s", qname, exc)
            stats.skipped += 1
        finally:
            record.set_state(SymbolState.COMPLETED)
            stats.symbol_runs.append(record)

    def _generate_with_cache(
        self,
        ctx: FunctionContext,
        *,
        pythonpath: list[str],
        cache_stats: GenerationCacheStats,
        budget: _LLMBudget,
    ) -> tuple[GeneratedTest, bool, RunResult | None]:
        operation = "generate"
        model = self._generator.model_name
        cache = self._generation_cache

        def _generate() -> GeneratedTest:
            if not budget.record("generate"):
                raise LLMBudgetExhausted("generate")
            return self._generator.generate(ctx, operation=operation)

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
        result = self._runner.run(test, pythonpath=pythonpath)
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

    def _repair_loop(
        self,
        ctx: FunctionContext,
        test: GeneratedTest,
        result: RunResult,
        pythonpath: list[str],
        budget: _LLMBudget,
        record: SymbolRunRecord,
    ) -> tuple[GeneratedTest, RunResult, bool, _LLMBudget, SymbolRunRecord]:
        repaired = False
        last_error_fp: str | None = None

        for attempt in range(1, self._max_repairs + 1):
            if result.passed:
                record.set_state(SymbolState.PASSED)
                break

            error_fp = _error_fingerprint(result)
            if error_fp == last_error_fp:
                record.stop_reason = "same_error_repeated"
                logger.info("  [repair] mesmo erro repetido — parando")
                break
            last_error_fp = error_fp

            if not budget.can_call():
                record.stop_reason = "llm_budget_exhausted"
                logger.warning("  [repair] orçamento LLM esgotado (%d/%d)",
                                 budget.calls, budget.max_calls)
                break

            logger.info("  [repair] tentativa %d/%d …", attempt, self._max_repairs)
            record.set_state(SymbolState.REPAIRING)
            try:
                if not budget.record(f"repair_{attempt}"):
                    record.stop_reason = "llm_budget_exhausted"
                    break
                test = self._repair_agent.repair(ctx, test, result, attempt=attempt)
                result = self._runner.run(test, pythonpath=pythonpath)
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

    def _coverage_loop(
        self,
        ctx: FunctionContext,
        test: GeneratedTest,
        result: RunResult,
        pythonpath: list[str],
        *,
        repaired: bool,
        budget: _LLMBudget,
        record: SymbolRunRecord,
    ) -> tuple[GeneratedTest, RunResult, bool, bool, _LLMBudget, SymbolRunRecord]:
        coverage_boosted = False
        approved_test = test
        approved_result = result

        if settings.MAX_COVERAGE_ROUNDS <= 0:
            return approved_test, approved_result, repaired, coverage_boosted, budget, record

        seen_signatures: set[str] = set()
        last_pct_before_regen: float | None = None

        for cov_round in range(1, settings.MAX_COVERAGE_ROUNDS + 1):
            record.set_state(SymbolState.COVERAGE_CHECKED)
            analyzer = CoverageAnalyzer(
                approved_test,
                ctx.file_path,
                target_function=ctx.qualified_name,
                pythonpath=pythonpath,
                threshold=settings.COVERAGE_THRESHOLD,
            )
            analyzer.run()
            summary = analyzer.generate_summary()
            current_pct = summary["line_coverage_percent"]

            if record.current_coverage_percent is not None:
                record.previous_coverage_percent = record.current_coverage_percent
            record.current_coverage_percent = current_pct

            if record.previous_coverage_percent is not None:
                logger.info(
                    "  [coverage] anterior=%s%%, atual=%s%% (threshold=%s%%)",
                    record.previous_coverage_percent,
                    current_pct,
                    summary["threshold_percent"],
                )
            else:
                logger.info(
                    "  [coverage] atual=%s%% (threshold=%s%%)",
                    current_pct,
                    summary["threshold_percent"],
                )

            if summary["meets_threshold"]:
                logger.info("  [coverage] threshold atingido — parando")
                break

            round_sig = coverage_round_signature(summary)
            if round_sig in seen_signatures:
                record.set_state(SymbolState.COVERAGE_STALLED)
                record.stop_reason = record.stop_reason or "identical_coverage_round"
                logger.info("  [coverage] rodada idêntica — parando")
                break
            seen_signatures.add(round_sig)

            if (
                settings.COVERAGE_STOP_ON_NO_IMPROVEMENT
                and last_pct_before_regen is not None
                and current_pct <= last_pct_before_regen
            ):
                record.set_state(SymbolState.COVERAGE_STALLED)
                record.stop_reason = record.stop_reason or "coverage_no_improvement"
                logger.info("  [coverage] sem melhoria — parando")
                break

            if not budget.can_call():
                record.stop_reason = record.stop_reason or "llm_budget_exhausted"
                logger.warning(
                    "  [coverage] orçamento LLM esgotado — mantendo teste aprovado",
                )
                break

            logger.info(
                "  [coverage] %s%% < %s%% — regenerando (%d/%d) …",
                current_pct,
                summary["threshold_percent"],
                cov_round,
                settings.MAX_COVERAGE_ROUNDS,
            )
            last_pct_before_regen = current_pct

            ctx = ctx.model_copy(update={
                "coverage_gaps": analyzer.gaps_for_prompt(),
                "coverage_summary": summary,
            })
            try:
                if not budget.record(f"coverage_{cov_round}"):
                    record.stop_reason = record.stop_reason or "llm_budget_exhausted"
                    break
                candidate = self._generator.generate(ctx, operation=f"coverage_{cov_round}")
            except Exception as exc:
                record.stop_reason = record.stop_reason or f"coverage_error:{exc}"
                logger.warning("  [coverage] erro na regeneração: %s", exc)
                break

            candidate_result = self._runner.run(candidate, pythonpath=pythonpath)
            if not candidate_result.passed:
                candidate, candidate_result, post_repair, budget, record = (
                    self._repair_loop(
                        ctx, candidate, candidate_result, pythonpath, budget, record,
                    )
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

        return approved_test, approved_result, repaired, coverage_boosted, budget, record

    def _save_test(
        self,
        workspace: RunWorkspace,
        qname: str,
        test: GeneratedTest,
        result: RunResult,
        repaired: bool,
        coverage_boosted: bool,
        stats: PipelineStats,
        *,
        ctx: FunctionContext | None = None,
    ) -> None:
        safe = re.sub(r"[^a-zA-Z0-9_]", "_", qname)
        dest = workspace.tests_dir / f"test_{safe}.py"
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

        if ctx is not None and self._generation_cache.enabled:
            coverage_summary = ctx.coverage_summary
            self._generation_cache.save(
                ctx,
                test,
                operation="generate",
                model=self._generator.model_name,
                coverage=coverage_summary,
            )
            try:
                self._retriever.index_generated_test(ctx.qualified_name, test.full_code)
            except Exception as exc:
                logger.warning("  [index_tests] %s", exc)

    def _validate_suite(self, workspace: RunWorkspace) -> SuiteValidationResult:
        logger.info("[validate] rodando pytest em %s …", workspace.tests_dir)
        result = self._runner.run_directory(
            workspace.tests_dir,
            pythonpath=[str(ROOT)],
            rootdir=ROOT,
        )

        if result.passed:
            logger.info(
                "  [validate] ok — %d passaram em %.2fs",
                result.num_passed,
                result.duration_seconds,
            )
        else:
            logger.warning(
                "  [validate] falhou (exit %d) — %d falharam, %d erros",
                result.exit_code,
                result.num_failed,
                result.num_errors,
            )
            if result.output.strip():
                for line in result.output.strip().splitlines()[-15:]:
                    logger.warning("  %s", line)

        validation_log = workspace.logs_dir / "pytest_validation.log"
        validation_log.write_text(result.output, encoding="utf-8")
        logger.info("[validate] log salvo em %s", validation_log)
        return result

    @staticmethod
    def _validation_payload(validation: SuiteValidationResult) -> dict:
        return {
            "passed": validation.passed,
            "exit_code": validation.exit_code,
            "tests_dir": validation.tests_dir,
            "num_passed": validation.num_passed,
            "num_failed": validation.num_failed,
            "num_errors": validation.num_errors,
            "duration_seconds": validation.duration_seconds,
        }

    def _log_summary(
        self,
        workspace: RunWorkspace,
        stats: PipelineStats,
        token_summary: str | None,
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
        if token_summary:
            logger.info("  Uso de tokens (OpenAI)")
            for line in token_summary.splitlines():
                logger.info(line)
        if settings.LOG_API_CALLS:
            logger.info("  Chamadas API         : %s", workspace.logs_dir / "api_calls")
        logger.info("=" * 52)
