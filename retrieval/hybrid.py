from __future__ import annotations

from dataclasses import dataclass

from config.settings import settings


@dataclass(frozen=True)
class HybridCandidate:
    qualified_name: str
    text: str
    vector_similarity: float = 0.0
    dependency_score: float = 0.0
    call_graph_score: float = 0.0

    @property
    def hybrid_score(self) -> float:
        return (
            settings.RETRIEVER_VECTOR_WEIGHT * self.vector_similarity
            + settings.RETRIEVER_DEPENDENCY_WEIGHT * self.dependency_score
            + settings.RETRIEVER_CALL_GRAPH_WEIGHT * self.call_graph_score
        )


def compute_hybrid_score(
    *,
    vector_similarity: float,
    dependency_score: float,
    call_graph_score: float,
) -> float:
    return (
        settings.RETRIEVER_VECTOR_WEIGHT * vector_similarity
        + settings.RETRIEVER_DEPENDENCY_WEIGHT * dependency_score
        + settings.RETRIEVER_CALL_GRAPH_WEIGHT * call_graph_score
    )


def rerank_candidates(
    candidates: list[HybridCandidate],
    *,
    top_k: int | None = None,
) -> list[HybridCandidate]:
    """Ordena candidatos por score híbrido descendente e retorna o top-k."""
    limit = top_k or settings.RETRIEVER_TOP_K
    ranked = sorted(candidates, key=lambda c: c.hybrid_score, reverse=True)
    return ranked[:limit]
