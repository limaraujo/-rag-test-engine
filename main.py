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
    return parser


def main(source_dir: str = ".") -> OrchestrationResult:
    orchestrator = OrchestratorAgent()
    return orchestrator.run(source_dir)


if __name__ == "__main__":
    args = build_parser().parse_args()
    main(source_dir=args.source_dir)
