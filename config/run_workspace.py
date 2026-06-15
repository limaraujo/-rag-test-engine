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
from parsers.source.path_filters import ScanResult
from parsers.source.symbol_filter import SymbolFilterResult


def _sanitize_slug(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]", "_", text)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "root"


def _path_to_slug(path: Path) -> str:
    return _sanitize_slug(path.as_posix().replace("/", "_"))


def source_slug(source_dir: Path, *, project_root: Path | None = None) -> str:
    """
    Nome seguro do diretório analisado para paths em ``runs/``.

    Usa o caminho relativo à raiz do engine quando possível, para que
    ``repositorios/code_katas/src`` vire ``repositorios_code_katas_src``
    em vez de apenas ``src``.
    """
    from config.settings import ROOT as engine_root

    resolved = source_dir.resolve()
    base = (project_root or engine_root).resolve()

    try:
        rel = resolved.relative_to(base)
        if rel in (Path("."), Path("")):
            return _sanitize_slug(resolved.name or "root")
        return _path_to_slug(rel)
    except ValueError:
        pass

    name = resolved.name
    if name and name not in (".", ""):
        return _sanitize_slug(name)

    return _sanitize_slug(resolved.parts[-1] if resolved.parts else "root")


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
    suite_metrics: dict | None = None,
) -> None:
    """Grava resumo final da execução em ``artifacts/run_summary.json``."""
    payload: dict = {
        **workspace.to_meta(),
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "stats": stats,
    }
    if token_usage is not None:
        payload["token_usage"] = token_usage
    if suite_metrics is not None:
        payload["suite_metrics"] = suite_metrics
    if settings.LOG_API_CALLS:
        payload["api_calls_dir"] = str(workspace.logs_dir / "api_calls")
    if validation:
        payload["validation"] = validation

    (workspace.artifacts_dir / "run_summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    if suite_metrics is not None:
        (workspace.artifacts_dir / "suite_metrics.json").write_text(
            json.dumps(suite_metrics, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def build_ingest_selection_payload(
    source_dir: Path,
    *,
    scan_result: ScanResult,
    filter_result: SymbolFilterResult,
) -> dict:
    """Monta JSON com arquivos e símbolos incluídos/excluídos na ingestão."""
    root = source_dir.resolve()
    included_files = [
        path.resolve().relative_to(root).as_posix()
        for path in scan_result.files
    ]
    return {
        "files": {
            "total_py_found": scan_result.total_py_found,
            "included_count": scan_result.included,
            "excluded_count": scan_result.excluded,
            "included": included_files,
            "excluded": [
                {"path": item.path, "reason": item.reason}
                for item in scan_result.excluded_files
            ],
        },
        "symbols": {
            "extracted_total": filter_result.stats.extracted_total,
            "selected_count": len(filter_result.kept),
            "filtered_count": filter_result.stats.filtered_total,
            "filter_stats": filter_result.stats.to_dict(),
            "selected": [
                {
                    "qualified_name": symbol.qualified_name,
                    "symbol_type": symbol.symbol_type,
                    "file_path": symbol.file_path,
                }
                for symbol in filter_result.kept
            ],
            "filtered": [
                {
                    "qualified_name": item.qualified_name,
                    "symbol_type": item.symbol_type,
                    "file_path": item.file_path,
                    "reason": item.reason,
                }
                for item in filter_result.filtered
            ],
        },
    }


def save_ingest_selection(
    workspace: RunWorkspace,
    *,
    scan_result: ScanResult,
    filter_result: SymbolFilterResult,
) -> Path:
    """Persiste arquivos/símbolos selecionados e ignorados em ``ingest_selection.json``."""
    payload = build_ingest_selection_payload(
        workspace.source_dir,
        scan_result=scan_result,
        filter_result=filter_result,
    )
    path = workspace.artifacts_dir / "ingest_selection.json"
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path
