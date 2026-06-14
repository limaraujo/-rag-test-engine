"""
Exemplo simples para o parser e para o pipeline de geração de testes.

Parser (sem API):
    uv run python mockes/exemplo.py
    → gera ``saida.json`` com símbolos deste arquivo

Pipeline completo com log de entradas/saídas da API:
    LOG_API_CALLS=true uv run python main.py mockes
    → logs em ``runs/mockes/<timestamp>/logs/api_calls/``

Só embeddings deste arquivo:
    LOG_API_CALLS=true uv run python mockes/embedding_demo.py mockes/exemplo.py
    → logs em ``logs/mockes/embedding_demo/<timestamp>/api_calls/``
"""
from dataclasses import dataclass
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ingest.parser import parse_repository_symbols


def soma(a: int, b: int) -> int:
    return a + b


@dataclass
class Calculadora:
    nome: str

    def multiplica(self, a: int, b: int) -> int:
        return a * b




def main() -> None:
    root = ROOT
    target_path = Path(__file__).resolve()
    output_path = root / "saida.json"
    extracted: list[dict] = []
    for symbol in parse_repository_symbols(str(root)):
        if Path(symbol.file_path).resolve() == target_path:
            extracted.append(symbol.model_dump())

    output_path.write_text(
        json.dumps(extracted, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Saved {len(extracted)} symbols to {output_path}")


if __name__ == "__main__":
    main()
