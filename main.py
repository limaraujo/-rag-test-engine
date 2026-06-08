"""
Pipeline de Geração de Testes com RAG
====================================

Uso:
    uv run python main.py [SOURCE_DIR] [OUTPUT_DIR]

Padrões:
    SOURCE_DIR = "."   (diretório de trabalho atual)
    OUTPUT_DIR = "generated_tests"

O que faz:
    1. Ingestão  — varre SOURCE_DIR, extrai símbolos via AST
    2. Indexação — gera embeddings dos símbolos e armazena no Qdrant
    3. Geração   — para cada símbolo, constrói FunctionContext, enriquece com RAG,
                  gera arquivo pytest com o LLM
    4. Execução  — executa cada teste gerado com pytest
    5. Reparo    — se um teste falhar, pede ao LLM para corrigi-lo (até MAX_REPAIRS vezes)
    6. Salvamento — escreve cada teste que passou em OUTPUT_DIR
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

from agents.repair import RepairAgent
from agents.test_generator import TestGeneratorAgent
from execution.runner import TestRunner
from ingest.parser import parse_repository_symbols
from retrieval.retriever import Retriever
from schemas.context import FunctionContext


MAX_REPAIRS = 2   # quantas tentativas de reparo com LLM por teste que falhar


def main(
    source_dir: str = ".",
    output_dir: str = "generated_tests",
) -> None:
    src = Path(source_dir).resolve()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Diretório fonte no PYTHONPATH para que os testes gerados possam importá-lo
    pythonpath = [str(src)]

    retriever    = Retriever()
    generator    = TestGeneratorAgent()
    runner       = TestRunner()
    repair_agent = RepairAgent()

    # ── 1. Ingestão ───────────────────────────────────────────────────────────
    print(f"[ingest] scanning {src} …")
    symbols = list(parse_repository_symbols(str(src)))
    print(f"[ingest] {len(symbols)} symbols found\n")

    # ── 2. Indexação ──────────────────────────────────────────────────────────
    print("[index] embedding and storing symbols in Qdrant …")
    total_indexed = retriever.index_symbols(symbols)
    print(f"[index] {total_indexed} symbols indexed\n")

    # ── 3–6. Geração → Execução → Reparo → Salvamento ─────────────────────────
    stats = {"ok": 0, "repaired": 0, "failed": 0, "skipped": 0}

    for symbol in symbols:
        qname = symbol.qualified_name
        print(f"[gen] {qname}")

        # Construir + enriquecer contexto
        ctx = FunctionContext.from_symbol(symbol)
        ctx = retriever.enrich(ctx, symbol)

        # Gerar
        try:
            test = generator.generate(ctx)
        except Exception as exc:
            print(f"  [skip] erro na geração: {exc}")
            stats["skipped"] += 1
            continue

        # Executar
        result = runner.run(test, pythonpath=pythonpath)

        # Loop de reparo
        repaired = False
        for attempt in range(1, MAX_REPAIRS + 1):
            if result.passed:
                break
            print(f"  [repair] tentativa {attempt}/{MAX_REPAIRS} …")
            try:
                test   = repair_agent.repair(ctx, test, result, attempt=attempt)
                result = runner.run(test, pythonpath=pythonpath)
                if result.passed:
                    repaired = True
            except Exception as exc:
                print(f"  [repair] erro: {exc}")
                break

        # Salvar / reportar
        if result.passed:
            safe = re.sub(r"[^a-zA-Z0-9_]", "_", qname)
            dest = out / f"test_{safe}.py"
            dest.write_text(test.full_code, encoding="utf-8")
            label = " (reparado)" if repaired else ""
            print(f"  [ok{label}] {result.num_passed} testes → {dest.name}")
            stats["ok"] += 1
            if repaired:
                stats["repaired"] += 1
        else:
            print(
                f"  [fail] {result.num_failed} falharam, "
                f"{result.num_errors} erros — ignorando"
            )
            stats["failed"] += 1

    # ── Resumo ────────────────────────────────────────────────────────────────
    total = stats["ok"] + stats["failed"] + stats["skipped"]
    print("\n" + "=" * 52)
    print(f"  Símbolos processados : {total}")
    print(f"  Testes salvos        : {stats['ok']} ({stats['repaired']} após reparo)")
    print(f"  Falharam (descartados): {stats['failed']}")
    print(f"  Ignorados (erros)    : {stats['skipped']}")
    print(f"  Diretório de saída   : {out}")
    print("=" * 52)


if __name__ == "__main__":
    _src = sys.argv[1] if len(sys.argv) > 1 else "."
    _out = sys.argv[2] if len(sys.argv) > 2 else "generated_tests"
    main(source_dir=_src, output_dir=_out)