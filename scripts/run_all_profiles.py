"""Executa os 4 perfis de teste em sequência sobre o mesmo SOURCE_DIR."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from config.run_profiles import PROFILE_CHOICES, describe_profiles
from main import main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Roda sem-rag, rag-limitado, rag-completo e com-cache em sequência.",
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
    return parser


def run_all(source_dir: str, *, allow_risky_source: bool = False) -> int:
    failures: list[str] = []
    run_group = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"run_group: {run_group}", flush=True)
    print("layout: runs/<repo>/{run_group}/<profile>/", flush=True)

    for profile in PROFILE_CHOICES:
        print(f"\n=== profile: {profile} ===", flush=True)
        try:
            result = main(
                source_dir,
                allow_risky_source=allow_risky_source,
                profile=profile,
                run_group=run_group,
            )
            print(f"  workspace: {result.workspace.root}", flush=True)
            print(
                f"  ok={result.stats.ok} failed={result.stats.failed} "
                f"cache_hits={result.generation_cache.hits}",
                flush=True,
            )
            if result.token_summary:
                print(result.token_summary, flush=True)
        except Exception as exc:
            failures.append(f"{profile}: {exc}")
            print(f"  ERRO: {exc}", file=sys.stderr, flush=True)

    if failures:
        print("\nFalhas:", file=sys.stderr)
        for item in failures:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("\nTodos os perfis concluíram.", flush=True)
    return 0


if __name__ == "__main__":
    args = build_parser().parse_args()
    raise SystemExit(run_all(args.source_dir, allow_risky_source=args.allow_risky_source))
