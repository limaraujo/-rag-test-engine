"""Heurísticas de qualidade e gating para enriquecimento RAG."""

from __future__ import annotations

from pathlib import Path

from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from retrieval.hybrid import HybridCandidate
from config.settings import settings


def parse_symbol_line(text: str) -> str | None:
    """Extrai qualified_name de ``symbol: foo.bar\\n...``."""
    stripped = text.strip()
    if stripped.startswith("symbol:"):
        first = stripped.split("\n", 1)[0]
        name = first.split(":", 1)[1].strip()
        return name or None
    return None


def should_apply_rag(
    symbol: ExtractedSymbol,
    *,
    caller_qnames: set[str],
    callee_qnames: set[str],
    dependency_qnames: set[str],
) -> bool:
    """
    Símbolos isolados e triviais raramente se beneficiam de vizinhos vetoriais.

    Mantém RAG quando há vizinhos de grafo, complexidade ou exceções explícitas.
    """
    if not settings.RAG_SKIP_ISOLATED_SYMBOLS:
        return True

    if caller_qnames or callee_qnames or dependency_qnames:
        return True
    if symbol.branches > settings.RAG_MIN_BRANCHES_FOR_ENRICHMENT:
        return True
    if symbol.exceptions or symbol.dependencies:
        return True
    if symbol.class_name:
        return True
    return False


def same_module(symbol: ExtractedSymbol, other: ExtractedSymbol) -> bool:
    return Path(symbol.file_path).parent.resolve() == Path(other.file_path).parent.resolve()


def filter_hybrid_candidates(
    ranked: list[HybridCandidate],
    *,
    graph_qnames: set[str],
    top_k: int,
) -> list[HybridCandidate]:
    """Mantém vizinhos de grafo; exige score mínimo para candidatos só vetoriais."""
    min_score = settings.RAG_MIN_HYBRID_SCORE
    kept: list[HybridCandidate] = []
    for candidate in ranked:
        if candidate.qualified_name in graph_qnames:
            kept.append(candidate)
        elif candidate.hybrid_score >= min_score:
            kept.append(candidate)
        if len(kept) >= top_k:
            break
    return kept[:top_k]


def exclude_graph_from_related(
    related: list[str],
    graph_qnames: set[str],
) -> list[str]:
    """Evita duplicar callees/callers/deps na seção ``related_functions``."""
    filtered: list[str] = []
    for item in related:
        qname = parse_symbol_line(item)
        if qname and qname in graph_qnames:
            continue
        filtered.append(item)
    return filtered
