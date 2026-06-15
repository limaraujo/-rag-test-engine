"""Executa perfis de teste em sequência com protocolo justo para RAG e cache."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.run_profiles import BATCH_PROFILE_SEQUENCE, PROFILE_CHOICES, describe_profiles
from main import main


@dataclass(frozen=True)
class BatchStep:
    profile: str
    clear_cache_after: bool


def _load_clear_cache():
    spec = importlib.util.spec_from_file_location(
        "clear_cache",
        ROOT / "scripts" / "clear_cache.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.clear_generation_cache


def fair_batch_steps() -> list[BatchStep]:
    """
    Protocolo justo (padrão):

    - Limpa cache antes do lote (RAG comparado sem resíduo de cache).
    - sem-rag / rag-limitado / rag-completo: limpa cache após cada um.
    - com-cache (1ª passagem): popula cache persistente — não limpa.
    - com-cache-rerun (2ª passagem): mede hits — limpa cache ao final.
    """
    steps: list[BatchStep] = []
    for profile in PROFILE_CHOICES:
        steps.append(BatchStep(profile, clear_cache_after=profile != "com-cache"))
    steps.append(BatchStep("com-cache-rerun", clear_cache_after=True))
    return steps


def legacy_batch_steps() -> list[BatchStep]:
    """Comportamento antigo: limpa cache após cada perfil (inclui com-cache)."""
    return [BatchStep(profile, True) for profile in PROFILE_CHOICES]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Roda sem-rag, rag-limitado, rag-completo, com-cache e com-cache-rerun "
            "em sequência."
        ),
        epilog=describe_profiles(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        default="mockes",
        help="diretório fonte (padrão: mockes)",
    )
    parser.add_argument(
        "--allow-risky-source",
        action="store_true",
        help="repassa --allow-risky-source para cada execução",
    )
    parser.add_argument(
        "--protocol",
        choices=("fair", "legacy"),
        default="fair",
        help=(
            "fair (padrão): RAG sem cache; com-cache popula cache; "
            "com-cache-rerun mede hits. "
            "legacy: limpa cache após cada perfil (sem 2ª passagem)."
        ),
    )
    return parser


def run_all(
    source_dir: str,
    *,
    allow_risky_source: bool = False,
    protocol: str = "fair",
) -> int:
    failures: list[str] = []
    run_group = datetime.now().strftime("%Y%m%d_%H%M%S")
    steps = fair_batch_steps() if protocol == "fair" else legacy_batch_steps()

    print(f"run_group: {run_group}", flush=True)
    print(f"protocol: {protocol}", flush=True)
    print("layout: runs/<repo>/{run_group}/<profile>/", flush=True)

    if protocol == "fair":
        removed = _load_clear_cache()()
        print(f"cache limpo (início do lote): {removed}", flush=True)

    for step in steps:
        profile = step.profile
        print(f"\n=== profile: {profile} ===", flush=True)
        try:
            result = main(
                source_dir,
                allow_risky_source=allow_risky_source,
                profile=profile,
                run_group=run_group,
            )
            gc = result.generation_cache
            print(f"  workspace: {result.workspace.root}", flush=True)
            print(
                f"  ok={result.stats.ok} failed={result.stats.failed} "
                f"cache_hits={gc.hits if gc else 0} "
                f"cache_misses={gc.misses if gc else 0} "
                f"llm_avoided={gc.llm_calls_avoided if gc else 0}",
                flush=True,
            )
            if result.token_summary:
                print(result.token_summary, flush=True)
        except Exception as exc:
            failures.append(f"{profile}: {exc}")
            print(f"  ERRO: {exc}", file=sys.stderr, flush=True)
        else:
            if step.clear_cache_after:
                removed = _load_clear_cache()()
                print(f"  cache limpo: {removed}", flush=True)

    if failures:
        print("\nFalhas:", file=sys.stderr)
        for item in failures:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("\nTodos os perfis concluíram.", flush=True)
    if protocol == "fair":
        print(
            "\nCompare RAG em sem-rag/rag-* e cache em com-cache vs com-cache-rerun:",
            flush=True,
        )
        print(
            f"  python scripts/compare_run_metrics.py runs/<slug>/{run_group}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    args = build_parser().parse_args()
    raise SystemExit(
        run_all(
            args.source_dir,
            allow_risky_source=args.allow_risky_source,
            protocol=args.protocol,
        )
    )
