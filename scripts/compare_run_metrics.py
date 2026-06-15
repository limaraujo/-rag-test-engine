"""Compara suite_metrics.json entre perfis de um run_group."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RAG_PROFILES = ("sem-rag", "rag-limitado", "rag-completo", "com-cache")
CACHE_PROFILES = ("com-cache", "com-cache-rerun")


def discover_profiles(base: Path) -> list[str]:
    found: list[str] = []
    for profile in (*RAG_PROFILES, "com-cache-rerun"):
        if (base / profile / "artifacts" / "suite_metrics.json").is_file():
            found.append(profile)
    return found


def load_metrics(base: Path, profile: str) -> dict:
    path = base / profile / "artifacts" / "suite_metrics.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_run_summary(base: Path, profile: str) -> dict | None:
    path = base / profile / "artifacts" / "run_summary.json"
    if not path.is_file():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def profile_summary(m: dict, *, run_summary: dict | None = None) -> dict:
    r = m["rates"]
    c = m["coverage"]
    cost = m["cost"]
    perf = m["performance"]
    prod = m["productivity"]
    validation_tests = m.get("tests", {})
    repaired = sum(1 for s in m["per_symbol"] if s.get("repaired"))

    gc = (run_summary or {}).get("stats", {}).get("generation_cache", {})

    return {
        "symbols_eligible": m.get("symbols_eligible"),
        "symbols_processed": m["symbols_processed"],
        "symbols_executable": m["symbols_executable"],
        "symbols_saved": m["symbols_saved"],
        "symbols_failed": m["symbols_failed"],
        "valid_generation_percent": r["valid_generation_percent"],
        "first_attempt_success_percent": r["first_attempt_success_percent"],
        "approval_percent": r["approval_percent"],
        "symbol_line_avg_percent": c["symbol_line_avg_percent"],
        "symbol_branch_avg_percent": c["symbol_branch_avg_percent"],
        "total_tokens": cost.get("total_tokens"),
        "total_llm_calls": cost.get("total_llm_calls"),
        "avg_tokens_per_symbol": cost.get("avg_tokens_per_symbol"),
        "repaired_symbols": repaired,
        "avg_duration_seconds_per_symbol": perf["avg_duration_seconds_per_symbol"],
        "valid_tests_saved_per_llm_call": prod["valid_tests_saved_per_llm_call"],
        "validation_tests_approved": validation_tests.get("approved"),
        "cache_hits": gc.get("hits"),
        "cache_misses": gc.get("misses"),
        "cache_llm_calls_avoided": gc.get("llm_calls_avoided"),
    }


def build_cache_benchmark(summaries: dict[str, dict]) -> dict | None:
    cold = summaries.get("com-cache")
    warm = summaries.get("com-cache-rerun")
    if not cold or not warm:
        return None

    cold_tokens = cold.get("total_tokens") or 0
    warm_tokens = warm.get("total_tokens") or 0
    reduction = None
    if cold_tokens > 0:
        reduction = round(100.0 * (cold_tokens - warm_tokens) / cold_tokens, 1)

    return {
        "cold_profile": "com-cache",
        "warm_profile": "com-cache-rerun",
        "cold_tokens": cold_tokens,
        "warm_tokens": warm_tokens,
        "token_reduction_percent": reduction,
        "cold_llm_calls": cold.get("total_llm_calls"),
        "warm_llm_calls": warm.get("total_llm_calls"),
        "cold_cache_hits": cold.get("cache_hits"),
        "warm_cache_hits": warm.get("cache_hits"),
        "warm_llm_calls_avoided": warm.get("cache_llm_calls_avoided"),
        "cold_symbols_saved": cold.get("symbols_saved"),
        "warm_symbols_saved": warm.get("symbols_saved"),
    }


def build_comparison(base: Path) -> dict:
    available = discover_profiles(base)
    if not available:
        raise FileNotFoundError(f"Nenhum suite_metrics.json em {base}")

    metrics = {
        p: load_metrics(base, p)
        for p in available
    }
    summaries = {
        p: profile_summary(
            metrics[p],
            run_summary=load_run_summary(base, p),
        )
        for p in available
    }

    rag_profiles = [p for p in RAG_PROFILES if p in summaries]
    failed_by: dict[str, dict[str, dict]] = {}
    for p in rag_profiles:
        failed_by[p] = {
            s["qualified_name"]: s
            for s in metrics[p]["per_symbol"]
            if not s["passed"]
        }

    all_failed = set()
    for p in rag_profiles:
        all_failed |= set(failed_by[p].keys())

    always_fail: set[str] = set()
    if rag_profiles:
        always_fail = set(failed_by[rag_profiles[0]].keys())
        for p in rag_profiles[1:]:
            always_fail &= set(failed_by[p].keys())

    only_sem_rag: list[str] = []
    if "sem-rag" in summaries:
        sem_ok = {
            s["qualified_name"] for s in metrics["sem-rag"]["per_symbol"] if s["passed"]
        }
        other_ok = set()
        for p in rag_profiles:
            if p == "sem-rag":
                continue
            other_ok |= {
                s["qualified_name"] for s in metrics[p]["per_symbol"] if s["passed"]
            }
        only_sem_rag = sorted(sem_ok - other_ok)

    failure_matrix = []
    for sym in sorted(all_failed):
        row: dict = {"qualified_name": sym}
        for p in rag_profiles:
            if sym in failed_by[p]:
                s = failed_by[p][sym]
                row[p] = {
                    "status": "fail",
                    "stop_reason": s.get("stop_reason") or "tests_failed",
                    "suite_executable": s.get("suite_executable"),
                    "repaired": s.get("repaired"),
                }
            else:
                row[p] = {"status": "ok"}
        failure_matrix.append(row)

    return {
        "run_group": base.name,
        "base_path": str(base),
        "profiles_available": available,
        "profiles": summaries,
        "cache_benchmark": build_cache_benchmark(summaries),
        "always_failed": sorted(always_fail),
        "only_sem_rag_saved": only_sem_rag,
        "failure_matrix": failure_matrix,
    }


def format_markdown_table(comparison: dict) -> str:
    lines: list[str] = []
    lines.append(f"# Métricas — `{comparison['run_group']}`")
    lines.append("")
    lines.append(f"Base: `{comparison['base_path']}`")
    lines.append("")

    cache_bench = comparison.get("cache_benchmark")
    if cache_bench:
        lines.append("## Benchmark de cache (com-cache → com-cache-rerun)")
        lines.append("")
        lines.append("| Métrica | 1ª passagem (fria) | 2ª passagem (quente) |")
        lines.append("| --- | --- | --- |")
        lines.append(
            f"| Tokens | {cache_bench['cold_tokens']:,} | {cache_bench['warm_tokens']:,} |"
        )
        lines.append(
            f"| Chamadas LLM | {cache_bench['cold_llm_calls']} | {cache_bench['warm_llm_calls']} |"
        )
        lines.append(
            f"| Cache hits | {cache_bench['cold_cache_hits']} | {cache_bench['warm_cache_hits']} |"
        )
        lines.append(
            f"| LLM evitadas | — | {cache_bench['warm_llm_calls_avoided']} |"
        )
        if cache_bench.get("token_reduction_percent") is not None:
            lines.append(
                f"| Redução de tokens | — | **{cache_bench['token_reduction_percent']}%** |"
            )
        lines.append("")

    lines.append("## Resumo por perfil (RAG)")
    lines.append("")
    headers = [
        "Perfil",
        "Salvos",
        "Falharam",
        "Válidos %",
        "1ª gen %",
        "Aprovação %",
        "Cov. linhas",
        "Tokens",
        "Cache hits",
        "LLM calls",
    ]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    rag_order = [p for p in RAG_PROFILES if p in comparison["profiles"]]
    for p in rag_order:
        s = comparison["profiles"][p]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{p}`",
                    str(s["symbols_saved"]),
                    str(s["symbols_failed"]),
                    f"{s['valid_generation_percent']:.1f}%",
                    f"{s['first_attempt_success_percent']:.1f}%",
                    f"{s['approval_percent']:.1f}%",
                    f"{s['symbol_line_avg_percent']:.1f}%",
                    f"{s['total_tokens']:,}",
                    str(s.get("cache_hits") if s.get("cache_hits") is not None else "—"),
                    str(s["total_llm_calls"]),
                ]
            )
            + " |"
        )

    if "com-cache-rerun" in comparison["profiles"]:
        s = comparison["profiles"]["com-cache-rerun"]
        lines.append("")
        lines.append("## 2ª passagem de cache (`com-cache-rerun`)")
        lines.append("")
        lines.append(f"- Símbolos salvos: {s['symbols_saved']}")
        lines.append(f"- Tokens: {s['total_tokens']:,}")
        lines.append(f"- Cache hits: {s.get('cache_hits', '—')}")
        lines.append(f"- LLM evitadas: {s.get('cache_llm_calls_avoided', '—')}")

    lines.append("")
    lines.append("## Símbolos que falharam em todos os perfis RAG")
    lines.append("")
    if comparison["always_failed"]:
        for sym in comparison["always_failed"]:
            lines.append(f"- `{sym}`")
    else:
        lines.append("_Nenhum._")

    lines.append("")
    lines.append("## Salvos só em sem-rag")
    lines.append("")
    if comparison["only_sem_rag_saved"]:
        for sym in comparison["only_sem_rag_saved"]:
            lines.append(f"- `{sym}`")
    else:
        lines.append("_Nenhum._")

    if comparison["failure_matrix"]:
        lines.append("")
        lines.append("## Matriz de falhas por símbolo (perfis RAG)")
        lines.append("")
        hdr = ["Símbolo"] + rag_order
        lines.append("| " + " | ".join(hdr) + " |")
        lines.append("| " + " | ".join(["---"] * len(hdr)) + " |")
        for row in comparison["failure_matrix"]:
            cells = [f"`{row['qualified_name']}`"]
            for p in rag_order:
                cell = row[p]
                if cell["status"] == "ok":
                    cells.append("OK")
                else:
                    reason = cell["stop_reason"] or "tests_failed"
                    cells.append(f"FALHA ({reason})")
            lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compara métricas entre perfis.")
    parser.add_argument(
        "run_dir",
        help="pasta do run_group, ex.: runs/repositorios_code_katas_src/20260615_000809",
    )
    parser.add_argument("--json-out", help="salvar comparação em JSON")
    parser.add_argument("--md-out", help="salvar tabela markdown")
    args = parser.parse_args()

    base = Path(args.run_dir)
    if not base.is_dir():
        print(f"Diretório não encontrado: {base}", file=sys.stderr)
        return 1

    try:
        comparison = build_comparison(base)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    md = format_markdown_table(comparison)
    print(md)

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(comparison, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"JSON: {out}", file=sys.stderr)

    if args.md_out:
        out = Path(args.md_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"Markdown: {out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
