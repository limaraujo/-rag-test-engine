"""Exemplo simples para o parser."""

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
    
    def divide(self, a: int, b: int) -> float:
        if b == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return a / b

    def potencia(self, a: int, b: int) -> int:
        if b < 0:
            raise ValueError("Expoente negativo não é permitido.")
        return a ** b


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
        encoding="utf-8"
    )
    print(f"Saved {len(extracted)} symbols to {output_path}")


if __name__ == "__main__":
    main()
