"""
Pipeline de Geração de Testes com RAG
====================================

Uso:
    uv run python main.py [SOURCE_DIR]
    uv run python main.py mockes --profile sem-rag
    uv run python main.py --help

Argumentos:
    SOURCE_DIR   Diretório Python a analisar (padrão: diretório atual).

Documentação completa: docs/CLI.md
"""
from __future__ import annotations

import argparse

from agents.orchestrator import OrchestratorAgent
from config.run_profiles import PROFILE_CHOICES, apply_run_profile, describe_profiles
from schemas.pipeline import OrchestrationResult


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Pipeline de geração de testes pytest com RAG.",
        epilog=describe_profiles() + "\n\nDemais opções vêm do .env — ver docs/CLI.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        default=".",
        help="diretório com código Python a analisar (padrão: %(default)s)",
    )
    parser.add_argument(
        "--profile",
        choices=PROFILE_CHOICES,
        default=None,
        metavar="PERFIL",
        help=(
            "perfil de teste: sem-rag, rag-limitado, rag-completo ou com-cache "
            "(sobrescreve RAG_MODE e GENERATION_CACHE_ENABLED durante a execução)"
        ),
    )
    parser.add_argument(
        "--allow-risky-source",
        action="store_true",
        help=(
            "continua mesmo com source_dir arriscado (raiz do engine ou muitos arquivos); "
            "necessário quando SOURCE_DIR_STRICT=true"
        ),
    )
    return parser


def _run_pipeline(
    source_dir: str,
    *,
    allow_risky_source: bool,
    run_group: str | None = None,
) -> OrchestrationResult:
    orchestrator = OrchestratorAgent()
    return orchestrator.run(
        source_dir,
        allow_risky=allow_risky_source,
        run_group=run_group,
    )


def main(
    source_dir: str = ".",
    *,
    allow_risky_source: bool = False,
    profile: str | None = None,
    run_group: str | None = None,
) -> OrchestrationResult:
    if profile:
        with apply_run_profile(profile):
            return _run_pipeline(
                source_dir,
                allow_risky_source=allow_risky_source,
                run_group=run_group,
            )
    return _run_pipeline(
        source_dir,
        allow_risky_source=allow_risky_source,
        run_group=run_group,
    )


if __name__ == "__main__":
    args = build_parser().parse_args()
    main(
        source_dir=args.source_dir,
        allow_risky_source=args.allow_risky_source,
        profile=args.profile,
    )
