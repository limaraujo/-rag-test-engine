"""
Pipeline de Geração de Testes com RAG
====================================

Uso:
    uv run python main.py [SOURCE_DIR]

Padrão:
    SOURCE_DIR = "."   (diretório de trabalho atual)

Cada execução cria uma pasta em ``runs/<nome_fonte>/<timestamp>/`` com:
    tests/       — testes gerados
    logs/        — pipeline.log
    artifacts/   — symbols.json, call_graph.json, dependency_graph.json, run_summary.json
"""
from __future__ import annotations

import sys

from agents.orchestrator import OrchestratorAgent
from schemas.pipeline import OrchestrationResult


def main(source_dir: str = ".") -> OrchestrationResult:
    orchestrator = OrchestratorAgent()
    return orchestrator.run(source_dir)


if __name__ == "__main__":
    _src = sys.argv[1] if len(sys.argv) > 1 else "."
    main(source_dir=_src)
