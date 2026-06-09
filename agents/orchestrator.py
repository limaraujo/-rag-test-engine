from __future__ import annotations

import logging
import re
from pathlib import Path

from agents.repair import RepairAgent
from agents.test_generator import TestGeneratorAgent
from config.logging_setup import setup_logging
from config.run_workspace import RunWorkspace, save_ingest_artifacts, save_run_summary
from config.settings import ROOT, settings
from execution.coverage_analyzer import CoverageAnalyzer
from execution.runner import RunResult, TestRunner
from ingest.call_graph import CallGraph
from ingest.dependency_graph import DependencyGraph
from ingest.models.ExtractedSymbol import ExtractedSymbol
from ingest.parser import parse_repository_graphs
from llm.usage_tracker import get_tracker, reset_tracker
from retrieval.retriever import Retriever
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from schemas.pipeline import OrchestrationResult, PipelineStats

logger = logging.getLogger(__name__)


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
    """

    def __init__(
        self,
        *,
        retriever: Retriever | None = None,
        generator: TestGeneratorAgent | None = None,
        runner: TestRunner | None = None,
        repair_agent: RepairAgent | None = None,
        max_repairs: int = 2,
    ) -> None:
        self._retriever = retriever or Retriever()
        self._generator = generator or TestGeneratorAgent()
        self._runner = runner or TestRunner()
        self._repair_agent = repair_agent or RepairAgent()
        self._max_repairs = max_repairs

    def run(self, source_dir: str | Path = ".") -> OrchestrationResult:
        src = Path(source_dir).resolve()
        workspace = RunWorkspace.create(src)

        log_file = setup_logging(workspace.logs_dir / "pipeline.log")
        logger.info("Workspace: %s", workspace.root)
        logger.info("Log: %s", log_file)

        if settings.AI_MODE == "offline":
            logger.warning("AI_MODE=offline — embeddings e LLM locais (sem API OpenAI)")

        reset_tracker()

        symbols, call_graph, dependency_graph = self._ingest(src, workspace)
        indexed, cache_hits = self._index(symbols)
        stats = self._process_symbols(
            symbols,
            workspace=workspace,
            call_graph=call_graph,
            dependency_graph=dependency_graph,
            source_dir=src,
        )

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
            },
            token_summary=token_summary,
        )
        self._log_summary(workspace, stats, token_summary)

        return OrchestrationResult(
            workspace=workspace,
            stats=stats,
            indexed=indexed,
            cache_hits=cache_hits,
            token_summary=token_summary,
        )

    def _ingest(
        self,
        src: Path,
        workspace: RunWorkspace,
    ) -> tuple[list[ExtractedSymbol], CallGraph, DependencyGraph]:
        logger.info("[ingest] scanning %s …", src)
        symbols, call_graph, dependency_graph = parse_repository_graphs(str(src))
        logger.info("[ingest] %d symbols found", len(symbols))
        logger.info(
            "[ingest] call graph: %d nodes, dependency graph: %d nodes",
            len(call_graph.nodes),
            len(dependency_graph.nodes),
        )

        save_ingest_artifacts(
            workspace,
            symbols=symbols,
            call_graph=call_graph,
            dependency_graph=dependency_graph,
        )
        logger.info("[ingest] artefatos salvos em %s", workspace.artifacts_dir)
        return symbols, call_graph, dependency_graph

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
    ) -> PipelineStats:
        stats = PipelineStats()
        symbols_by_name = {symbol.qualified_name: symbol for symbol in symbols}
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
            test = self._generator.generate(ctx)
        except Exception as exc:
            logger.warning("  [skip] erro na geração: %s", exc)
            stats.skipped += 1
            return

        result = self._runner.run(test, pythonpath=pythonpath)
        test, result, repaired = self._repair_loop(ctx, test, result, pythonpath)

        coverage_boosted = False
        if result.passed:
            test, result, repaired, coverage_boosted = self._coverage_loop(
                ctx,
                test,
                result,
                pythonpath,
                repaired=repaired,
            )

        if result.passed:
            self._save_test(workspace, qname, test, result, repaired, coverage_boosted, stats)
        else:
            logger.warning(
                "  [fail] %d falharam, %d erros — ignorando",
                result.num_failed,
                result.num_errors,
            )
            stats.failed += 1

    def _repair_loop(
        self,
        ctx: FunctionContext,
        test: GeneratedTest,
        result: RunResult,
        pythonpath: list[str],
    ) -> tuple[GeneratedTest, RunResult, bool]:
        repaired = False
        for attempt in range(1, self._max_repairs + 1):
            if result.passed:
                break
            logger.info("  [repair] tentativa %d/%d …", attempt, self._max_repairs)
            try:
                test = self._repair_agent.repair(ctx, test, result, attempt=attempt)
                result = self._runner.run(test, pythonpath=pythonpath)
                if result.passed:
                    repaired = True
            except Exception as exc:
                logger.warning("  [repair] erro: %s", exc)
                break
        return test, result, repaired

    def _coverage_loop(
        self,
        ctx: FunctionContext,
        test: GeneratedTest,
        result: RunResult,
        pythonpath: list[str],
        *,
        repaired: bool,
    ) -> tuple[GeneratedTest, RunResult, bool, bool]:
        coverage_boosted = False

        for cov_round in range(1, settings.MAX_COVERAGE_ROUNDS + 1):
            analyzer = CoverageAnalyzer(
                test,
                ctx.file_path,
                target_function=ctx.qualified_name,
                pythonpath=pythonpath,
                threshold=settings.COVERAGE_THRESHOLD,
            )
            analyzer.run()
            summary = analyzer.generate_summary()

            if summary["meets_threshold"]:
                logger.info(
                    "  [coverage] %s%% (≥ %s%%)",
                    summary["line_coverage_percent"],
                    summary["threshold_percent"],
                )
                break

            logger.info(
                "  [coverage] %s%% < %s%% — regenerando (%d/%d) …",
                summary["line_coverage_percent"],
                summary["threshold_percent"],
                cov_round,
                settings.MAX_COVERAGE_ROUNDS,
            )
            ctx = ctx.model_copy(update={
                "coverage_gaps": analyzer.gaps_for_prompt(),
                "coverage_summary": summary,
            })
            try:
                test = self._generator.generate(ctx)
            except Exception as exc:
                logger.warning("  [coverage] erro na regeneração: %s", exc)
                break

            result = self._runner.run(test, pythonpath=pythonpath)
            if not result.passed:
                test, result, post_repair = self._repair_loop(
                    ctx, test, result, pythonpath,
                )
                repaired = repaired or post_repair
                if not result.passed:
                    break

            coverage_boosted = True

        return test, result, repaired, coverage_boosted

    def _save_test(
        self,
        workspace: RunWorkspace,
        qname: str,
        test: GeneratedTest,
        result: RunResult,
        repaired: bool,
        coverage_boosted: bool,
        stats: PipelineStats,
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

    def _log_summary(
        self,
        workspace: RunWorkspace,
        stats: PipelineStats,
        token_summary: str | None,
    ) -> None:
        logger.info("")
        logger.info("=" * 52)
        logger.info("  Símbolos processados : %d", stats.total)
        logger.info(
            "  Testes salvos        : %d (%d após reparo, %d com boost de cobertura)",
            stats.ok,
            stats.repaired,
            stats.coverage_boosted,
        )
        logger.info("  Falharam (descartados): %d", stats.failed)
        logger.info("  Ignorados (erros)    : %d", stats.skipped)
        logger.info("  Workspace            : %s", workspace.root)
        logger.info("  Testes               : %s", workspace.tests_dir)
        logger.info("  Artefatos            : %s", workspace.artifacts_dir)
        if token_summary:
            logger.info("  Uso de tokens (OpenAI)")
            for line in token_summary.splitlines():
                logger.info(line)
        logger.info("=" * 52)
