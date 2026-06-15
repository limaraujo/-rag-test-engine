from __future__ import annotations

import logging
from pathlib import Path

from agents.policies.llm_budget import LLMBudget, LLMBudgetExhausted, _LLMBudget, _error_fingerprint
from agents.repair import RepairAgent
from agents.services.coverage_cycle import run_coverage_loop
from agents.services.generation_service import generate_with_cache, save_approved_test
from agents.services.pipeline_logging import (
    collect_ignored_symbols,
    log_pytest_result,
    log_run_summary,
    validation_payload,
)
from agents.services.repair_cycle import run_repair_loop
from agents.test_generator import TestGeneratorAgent
from cache.generation_cache import GenerationCache
from config.logging_setup import setup_logging
from config.run_workspace import RunWorkspace, save_ingest_artifacts, save_run_summary
from config.settings import ROOT, settings
from config.source_guard import ensure_source_dir_allowed
from execution.runner import SuiteValidationResult, TestRunner
from ingest.call_graph import CallGraph
from ingest.dependency_graph import DependencyGraph
from ingest.models.ExtractedSymbol import ExtractedSymbol
from ingest.symbol_filter import SymbolFilterStats, filter_symbols
from ingest.path_filters import ScanResult, emit_scan_warnings, scan_python_files
from ingest.parser import parse_repository_graphs
from llm.call_logger import setup_api_call_logging
from llm.usage_tracker import get_tracker, reset_tracker
from retrieval.retriever import Retriever
from schemas.context import FunctionContext
from schemas.pipeline import (
    OrchestrationResult,
    PipelineStats,
    SymbolRunRecord,
    SymbolState,
)
logger = logging.getLogger(__name__)

__all__ = [
    "LLMBudgetExhausted",
    "OrchestratorAgent",
    "_LLMBudget",
    "_error_fingerprint",
]


class OrchestratorAgent:
    """
    Orquestra o pipeline completo de geração de testes com RAG.

    Fases:
        1. Ingestão  — parser + grafos + artefatos
        2. Indexação — embeddings no Qdrant
        3. Geração   — LLM + RAG por símbolo
        4. Execução  — pytest por símbolo
        5. Reparo    — LLM corrige falhas
        6. Cobertura — pytest+coverage (--branch); regenera se abaixo do threshold
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

    def run(
        self,
        source_dir: str | Path = ".",
        *,
        allow_risky: bool = False,
    ) -> OrchestrationResult:
        src = Path(source_dir).resolve()
        scan_result = scan_python_files(src)
        ensure_source_dir_allowed(
            src,
            allow_risky=allow_risky,
            scan_result=scan_result,
        )
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
            self._ingest(src, workspace, scan_result=scan_result)
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

        token_usage_payload = None
        token_summary_text = None
        if settings.AI_MODE != "offline":
            tracker = get_tracker()
            token_usage_payload = tracker.build_summary(
                embedding_cache_hits=cache_hits,
                generation_cache_hits=stats.generation_cache.hits,
                llm_calls_avoided=stats.generation_cache.llm_calls_avoided,
                ignored_symbols=collect_ignored_symbols(filter_stats, stats),
            )
            token_summary_text = tracker.format_summary()

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
                "embedding_cache_hits": cache_hits,
                "symbol_runs": [record.to_dict() for record in stats.symbol_runs],
            },
            token_usage=token_usage_payload,
            validation=validation_payload(validation),
        )
        log_run_summary(
            workspace,
            stats,
            token_summary_text,
            validation=validation,
            filter_stats=filter_stats,
        )

        return OrchestrationResult(
            workspace=workspace,
            stats=stats,
            indexed=indexed,
            cache_hits=cache_hits,
            token_summary=token_summary_text,
            token_usage=token_usage_payload,
            validation=validation,
            generation_cache=stats.generation_cache,
        )

    def _ingest(
        self,
        src: Path,
        workspace: RunWorkspace,
        *,
        scan_result: ScanResult | None = None,
    ) -> tuple[
        list[ExtractedSymbol],
        list[ExtractedSymbol],
        CallGraph,
        DependencyGraph,
        SymbolFilterStats,
    ]:
        logger.info("[ingest] scanning %s …", src)
        scan_result = scan_result or scan_python_files(src)
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
        budget = LLMBudget(settings.MAX_LLM_CALLS_PER_SYMBOL)
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
                test, from_cache, cached_result = generate_with_cache(
                    ctx,
                    pythonpath=pythonpath,
                    cache_stats=stats.generation_cache,
                    budget=budget,
                    generator=self._generator,
                    runner=self._runner,
                    generation_cache=self._generation_cache,
                )
            except LLMBudgetExhausted:
                record.stop_reason = "llm_budget_exhausted"
                stats.failed += 1
                return
            record.from_cache = from_cache
            repaired = False

            if from_cache and cached_result is not None:
                result = cached_result
                record.record_pytest_result(result)
                log_pytest_result(result)
                if result.passed:
                    record.set_state(SymbolState.PASSED)
                else:
                    record.set_state(SymbolState.TEST_FAILED)
            else:
                record.set_state(SymbolState.GENERATED)
                result = self._runner.run(test, pythonpath=pythonpath)
                record.record_pytest_result(result)
                log_pytest_result(result)
                if result.passed:
                    record.set_state(SymbolState.PASSED)
                else:
                    record.set_state(SymbolState.TEST_FAILED)
                    test, result, repaired, budget, record = run_repair_loop(
                        ctx,
                        test,
                        result,
                        pythonpath,
                        budget,
                        record,
                        repair_agent=self._repair_agent,
                        runner=self._runner,
                        max_repairs=self._max_repairs,
                    )

            coverage_boosted = False
            if result.passed:
                test, result, repaired, coverage_boosted, budget, record = (
                    run_coverage_loop(
                        ctx,
                        test,
                        result,
                        pythonpath,
                        budget,
                        record,
                        repaired=repaired,
                        generator=self._generator,
                        runner=self._runner,
                        repair_agent=self._repair_agent,
                        max_repairs=self._max_repairs,
                    )
                )

            record.passed = result.passed
            record.repaired = repaired
            record.coverage_boosted = coverage_boosted
            record.llm_calls = budget.calls

            if result.passed:
                save_approved_test(
                    workspace,
                    qname,
                    test,
                    result,
                    repaired,
                    coverage_boosted,
                    stats,
                    ctx=ctx,
                    generator=self._generator,
                    generation_cache=self._generation_cache,
                    retriever=self._retriever,
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
