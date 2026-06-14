"""
Pipeline de Geração de Testes com RAG
====================================

Uso:
    uv run python main.py [SOURCE_DIR]
    uv run python main.py --help

Argumentos:
    SOURCE_DIR   Diretório Python a analisar (padrão: diretório atual).

Documentação completa: docs/CLI.md
"""
from __future__ import annotations

import argparse

from agents.orchestrator import OrchestratorAgent
from schemas.pipeline import OrchestrationResult


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Pipeline de geração de testes pytest com RAG.",
        epilog="Demais opções (modelo, Qdrant, logs de API) vêm do .env — ver docs/CLI.md.",
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        default=".",
        help="diretório com código Python a analisar (padrão: %(default)s)",
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


def main(
    source_dir: str = ".",
    *,
    allow_risky_source: bool = False,
) -> OrchestrationResult:
    orchestrator = OrchestratorAgent()
    return orchestrator.run(source_dir, allow_risky=allow_risky_source)


if __name__ == "__main__":
    args = build_parser().parse_args()
    main(source_dir=args.source_dir, allow_risky_source=args.allow_risky_source)
