from __future__ import annotations

from pydantic import BaseModel, Field


class RetrievalContext(BaseModel):
    """
    Contexto recuperado pela busca híbrida (vetorial + grafos).

    Combina similaridade semântica (Qdrant), relações do call graph
    e relações do dependency graph em um único pacote de contexto RAG.
    """

    related_functions: list[str] = Field(
        default_factory=list,
        description=(
            "Funções reordenadas por score híbrido "
            "(vetor + dependency graph + call graph). Top 10."
        ),
    )
    dependency_functions: list[str] = Field(
        default_factory=list,
        description="Código de símbolos ligados via dependency graph.",
    )
    caller_functions: list[str] = Field(
        default_factory=list,
        description="Código de funções que chamam o símbolo alvo (call graph).",
    )
    callee_functions: list[str] = Field(
        default_factory=list,
        description="Código de funções chamadas pelo símbolo alvo (call graph).",
    )
    similar_tests: list[str] = Field(
        default_factory=list,
        description="Testes semanticamente similares recuperados do Qdrant. Top 10.",
    )


class RetrievalMetrics(BaseModel):
    """Métricas de uma execução de busca híbrida, para logs e observabilidade."""

    qualified_name: str
    vector_candidates: int = 0
    dependency_neighbors: int = 0
    call_graph_neighbors: int = 0
    reranked_candidates: int = 0
    top_hybrid_score: float = 0.0
    avg_hybrid_score: float = 0.0
    similar_tests_count: int = 0

    def log_summary(self) -> str:
        return (
            f"retrieval[{self.qualified_name}] "
            f"vector={self.vector_candidates} "
            f"dep_neighbors={self.dependency_neighbors} "
            f"call_neighbors={self.call_graph_neighbors} "
            f"reranked={self.reranked_candidates} "
            f"top_score={self.top_hybrid_score:.3f} "
            f"avg_score={self.avg_hybrid_score:.3f} "
            f"similar_tests={self.similar_tests_count}"
        )
