from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from config.settings import settings
from parsers.source.call_graph import CallGraph
from parsers.source.dependency_graph import DependencyGraph
from parsers.source.models.ExtractedSymbol import ExtractedSymbol


def source_slug(source_dir: Path) -> str:
    """Nome seguro do repositório/diretório analisado para paths em ``runs/``."""
    name = source_dir.name
    if name in (".", ""):
        name = source_dir.resolve().name or "root"
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def resolve_workspace_root(
    source_dir: Path,
    *,
    runs_base: Path,
    profile: str | None = None,
    run_group: str | None = None,
    timestamp: str | None = None,
) -> Path:
    """
    Monta o path do workspace.

    Layout:
    - sem perfil: ``runs/<repo>/<timestamp>/``
    - com perfil: ``runs/<repo>/<profile>/<timestamp>/``
    - lote (4 perfis): ``runs/<repo>/<run_group>/<profile>/``
    """
    slug = source_slug(source_dir)
    ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")

    if profile and run_group:
        return runs_base / slug / run_group / profile
    if profile:
        return runs_base / slug / profile / ts
    return runs_base / slug / ts


@dataclass(frozen=True)
class RunWorkspace:
    """Diretório de uma execução: testes, logs e artefatos."""

    root: Path
    source_dir: Path
    source_slug: str
    profile: str | None
    run_group: str | None
    tests_dir: Path
    logs_dir: Path
    artifacts_dir: Path

    @classmethod
    def create(
        cls,
        source_dir: Path,
        *,
        runs_base: Path | None = None,
        profile: str | None = None,
        run_group: str | None = None,
    ) -> RunWorkspace:
        base = runs_base or Path(settings.RUNS_DIR)
        resolved = source_dir.resolve()
        slug = source_slug(resolved)
        root = resolve_workspace_root(
            resolved,
            runs_base=base,
            profile=profile,
            run_group=run_group,
        )

        workspace = cls(
            root=root,
            source_dir=resolved,
            source_slug=slug,
            profile=profile,
            run_group=run_group,
            tests_dir=root / "tests",
            logs_dir=root / "logs",
            artifacts_dir=root / "artifacts",
        )
        for path in (workspace.tests_dir, workspace.logs_dir, workspace.artifacts_dir):
            path.mkdir(parents=True, exist_ok=True)
        return workspace

    def to_meta(self) -> dict[str, str | None]:
        return {
            "source_dir": str(self.source_dir),
            "source_slug": self.source_slug,
            "profile": self.profile,
            "run_group": self.run_group,
            "workspace": str(self.root),
            "tests_dir": str(self.tests_dir),
            "logs_dir": str(self.logs_dir),
            "artifacts_dir": str(self.artifacts_dir),
        }


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
                **workspace.to_meta(),
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
        **workspace.to_meta(),
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
