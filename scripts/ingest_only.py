"""
Executa apenas a fase de ingestão (parser + grafos), sem LLM, Qdrant ou pytest.

Uso:
    python scripts/ingest_only.py repositorios/code_katas/src
    python scripts/ingest_only.py mockes --allow-risky-source
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.logging_setup import setup_logging
from config.run_workspace import RunWorkspace, save_ingest_artifacts, save_ingest_selection
from config.source_guard import ensure_source_dir_allowed
from agents.services.pipeline_logging import log_ingest_selection
from parsers.source.path_filters import emit_scan_warnings, scan_python_files
from parsers.source.parser import parse_repository_graphs
from parsers.source.symbol_filter import filter_symbols

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingestão estática: parser, call graph e dependency graph.",
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        default=".",
        help="diretório com código Python a analisar",
    )
    parser.add_argument(
        "--allow-risky-source",
        action="store_true",
        help="continua mesmo com source_dir arriscado (SOURCE_DIR_STRICT)",
    )
    return parser


def run_ingest(
    source_dir: str | Path,
    *,
    allow_risky: bool = False,
) -> RunWorkspace:
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
    logger.info("Repositório: %s (%s)", workspace.source_slug, workspace.source_dir)
    logger.info("Log: %s", log_file)
    logger.info("[ingest] scanning %s …", src)
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
    selection_path = save_ingest_selection(
        workspace,
        scan_result=scan_result,
        filter_result=filter_result,
    )
    log_ingest_selection(
        src,
        scan_result,
        filter_result,
        selection_artifact=selection_path,
    )

    return workspace


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_ingest(args.source_dir, allow_risky=args.allow_risky_source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
