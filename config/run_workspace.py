from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from config.settings import settings
from ingest.call_graph import CallGraph
from ingest.dependency_graph import DependencyGraph
from ingest.models.ExtractedSymbol import ExtractedSymbol


def _source_slug(source_dir: Path) -> str:
    name = source_dir.name
    if name in (".", ""):
        name = source_dir.resolve().name or "root"
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


@dataclass(frozen=True)
class RunWorkspace:
    """Diretório de uma execução: testes, logs e artefatos do ingest."""

    root: Path
    source_dir: Path
    tests_dir: Path
    logs_dir: Path
    artifacts_dir: Path

    @classmethod
    def create(
        cls,
        source_dir: Path,
        *,
        runs_base: Path | None = None,
    ) -> RunWorkspace:
        base = runs_base or Path(settings.RUNS_DIR)
        slug = _source_slug(source_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        root = base / slug / timestamp

        workspace = cls(
            root=root,
            source_dir=source_dir.resolve(),
            tests_dir=root / "tests",
            logs_dir=root / "logs",
            artifacts_dir=root / "artifacts",
        )
        for path in (workspace.tests_dir, workspace.logs_dir, workspace.artifacts_dir):
            path.mkdir(parents=True, exist_ok=True)
        return workspace


def save_ingest_artifacts(
    workspace: RunWorkspace,
    *,
    symbols: list[ExtractedSymbol],
    call_graph: CallGraph,
    dependency_graph: DependencyGraph,
) -> None:
    """Persiste saída do parser e dos grafos em ``workspace/artifacts``."""
    artifacts = workspace.artifacts_dir

    (artifacts / "symbols.json").write_text(
        json.dumps(
            [symbol.model_dump() for symbol in symbols],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (artifacts / "call_graph.json").write_text(
        call_graph.to_json(),
        encoding="utf-8",
    )
    (artifacts / "dependency_graph.json").write_text(
        dependency_graph.to_json(),
        encoding="utf-8",
    )
    (artifacts / "run_meta.json").write_text(
        json.dumps(
            {
                "source_dir": str(workspace.source_dir),
                "symbol_count": len(symbols),
                "call_graph_nodes": len(call_graph.nodes),
                "dependency_graph_nodes": len(dependency_graph.nodes),
                "started_at": datetime.now().isoformat(timespec="seconds"),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def save_run_summary(
    workspace: RunWorkspace,
    *,
    stats: dict,
    token_usage: dict | str | None = None,
    validation: dict | None = None,
) -> None:
    """Grava resumo final da execução em ``artifacts/run_summary.json``."""
    payload: dict = {
        "workspace": str(workspace.root),
        "source_dir": str(workspace.source_dir),
        "tests_dir": str(workspace.tests_dir),
        "logs_dir": str(workspace.logs_dir),
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "stats": stats,
    }
    if token_usage is not None:
        payload["token_usage"] = token_usage
    if settings.LOG_API_CALLS:
        payload["api_calls_dir"] = str(workspace.logs_dir / "api_calls")
    if validation:
        payload["validation"] = validation

    (workspace.artifacts_dir / "run_summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
