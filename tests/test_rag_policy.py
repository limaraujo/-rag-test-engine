from __future__ import annotations

from retrieval.hybrid import HybridCandidate, compute_hybrid_score, rerank_candidates
from retrieval.rag_policy import (
    exclude_graph_from_related,
    filter_hybrid_candidates,
    should_apply_rag,
)
from tests.conftest import make_symbol


def test_should_skip_isolated_trivial_symbol(monkeypatch) -> None:
    monkeypatch.setattr("retrieval.rag_policy.settings.RAG_SKIP_ISOLATED_SYMBOLS", True)
    monkeypatch.setattr("retrieval.rag_policy.settings.RAG_MIN_BRANCHES_FOR_ENRICHMENT", 1)
    sym = make_symbol("add", "def add(a, b):\n    return a + b")
    assert should_apply_rag(sym, caller_qnames=set(), callee_qnames=set(), dependency_qnames=set()) is False


def test_should_apply_when_graph_neighbor_exists(monkeypatch) -> None:
    monkeypatch.setattr("retrieval.rag_policy.settings.RAG_SKIP_ISOLATED_SYMBOLS", True)
    sym = make_symbol("add", "def add(a, b):\n    return a + b")
    assert should_apply_rag(sym, caller_qnames={"sub"}, callee_qnames=set(), dependency_qnames=set()) is True


def test_filter_hybrid_keeps_graph_despite_low_score(monkeypatch) -> None:
    monkeypatch.setattr("retrieval.rag_policy.settings.RAG_MIN_HYBRID_SCORE", 0.9)
    ranked = [
        HybridCandidate("weak", "def weak(): pass", vector_similarity=0.1),
        HybridCandidate(
            "neighbor",
            "def neighbor(): pass",
            vector_similarity=0.2,
            call_graph_score=1.0,
        ),
    ]
    kept = filter_hybrid_candidates(ranked, graph_qnames={"neighbor"}, top_k=2)
    assert [c.qualified_name for c in kept] == ["neighbor"]


def test_exclude_graph_from_related() -> None:
    related = [
        "symbol: foo.callee\ndef callee(): pass",
        "symbol: distant\ndef distant(): pass",
    ]
    out = exclude_graph_from_related(related, {"foo.callee"})
    assert len(out) == 1
    assert "distant" in out[0]


def test_same_module_boost_in_hybrid_score(monkeypatch) -> None:
    monkeypatch.setattr("config.settings.settings.RAG_SAME_MODULE_BOOST", 0.2)
    base = compute_hybrid_score(vector_similarity=0.5, dependency_score=0.0, call_graph_score=0.0)
    boosted = compute_hybrid_score(
        vector_similarity=0.5,
        dependency_score=0.0,
        call_graph_score=0.0,
        same_module_score=1.0,
    )
    assert boosted == base + 0.2
