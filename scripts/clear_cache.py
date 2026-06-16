"""Remove caches persistentes do engine após uma execução."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import ROOT as ENGINE_ROOT, settings


def generation_cache_dir() -> Path:
    configured = (settings.GENERATION_CACHE_DIR or "").strip()
    if configured:
        path = Path(configured)
        return path if path.is_absolute() else ENGINE_ROOT / path
    return ENGINE_ROOT / ".cache" / "generation"


def clear_generation_cache() -> Path:
    cache_dir = generation_cache_dir()
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    return cache_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Limpa o cache persistente de geração (.cache/generation por padrão).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="apenas mostra o caminho que seria removido",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    cache_dir = generation_cache_dir()
    if args.dry_run:
        print(cache_dir)
        return 0
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        print(f"Cache removido: {cache_dir}")
    else:
        print(f"Nada a limpar: {cache_dir} não existe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
