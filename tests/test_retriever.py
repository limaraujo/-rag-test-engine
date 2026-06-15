from __future__ import annotations

import pytest

from parsers.source.call_graph import CallGraph, CallGraphNode
from parsers.source.dependency_graph import DependencyGraph, DependencyNode
from retrieval.hybrid import HybridCandidate, compute_hybrid_score, rerank_candidates
from retrieval.retriever import Retriever
from schemas.context import FunctionContext
from tests.conftest import TEST_DIM, make_record, make_symbol


# ── hybrid scoring ────────────────────────────────────────────────────────────


def test_compute_hybrid_score_formula(monkeypatch) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_VECTOR_WEIGHT", 0.5)
    monkeypatch.setattr("config.settings.settings.RETRIEVER_DEPENDENCY_WEIGHT", 0.3)
    monkeypatch.setattr("config.settings.settings.RETRIEVER_CALL_GRAPH_WEIGHT", 0.2)

    score = compute_hybrid_score(
        vector_similarity=0.8,
        dependency_score=1.0,
        call_graph_score=0.0,
    )
    assert score == pytest.approx(0.5 * 0.8 + 0.3 * 1.0 + 0.2 * 0.0)


def test_rerank_prioritizes_graph_boosted_candidate(monkeypatch) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_TOP_K_FUNCTIONS", 2)

    candidates = [
        HybridCandidate("low_vector", "def low(): pass", vector_similarity=0.9),
        HybridCandidate(
            "graph_neighbor",
            "def graph(): pass",
            vector_similarity=0.4,
            dependency_score=1.0,
            call_graph_score=1.0,
        ),
    ]
    ranked = rerank_candidates(candidates)
    assert [c.qualified_name for c in ranked] == ["graph_neighbor", "low_vector"]


def test_rerank_respects_top_k(monkeypatch) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_TOP_K_FUNCTIONS", 2)
    candidates = [
        HybridCandidate(f"f{i}", f"def f{i}(): pass", vector_similarity=i / 10)
        for i in range(5)
    ]
    ranked = rerank_candidates(candidates)
    assert len(ranked) == 2


# ── Retriever.enrich ──────────────────────────────────────────────────────────


def _upsert_symbol(store, qname: str, vector: list[float], text: str | None = None) -> None:
    store.upsert("symbols", [make_record(qname, vector, text=text)])


@pytest.fixture
def retriever(store, fake_embedder):
    return Retriever(store=store, embedder=fake_embedder)


def test_enrich_populates_retrieval_context(retriever, store, fake_embedder, monkeypatch) -> None:
    from retrieval.embeddings import embed_symbol

    monkeypatch.setattr("config.settings.settings.RETRIEVER_TOP_K_FUNCTIONS", 3)
    monkeypatch.setattr("config.settings.settings.RETRIEVER_SCORE_THRESHOLD", None)

    target = make_symbol("target", "def target(): return 1")
    neighbor = make_symbol("neighbor", "def neighbor(): return 2")

    store.upsert(
        "symbols",
        [embed_symbol(s, embedder=fake_embedder) for s in (target, neighbor)],
    )

    ctx = FunctionContext.from_symbol(target)
    enriched = retriever.enrich(ctx, target, symbols_by_name={"target": target, "neighbor": neighbor})

    assert enriched.retrieval_context is not None
    assert enriched.retrieval_context.related_functions
    assert enriched.related_functions == enriched.retrieval_context.related_functions


def test_enrich_excludes_self(retriever, store, fake_embedder, monkeypatch) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_SCORE_THRESHOLD", None)

    symbol = make_symbol("solo", "def solo(): pass")
    vec = [0.1] * TEST_DIM
    _upsert_symbol(store, "solo", vec, "def solo(): pass")

    ctx = FunctionContext.from_symbol(symbol)
    enriched = retriever.enrich(ctx, symbol, symbols_by_name={"solo": symbol})

    assert enriched.retrieval_context is not None
    assert enriched.retrieval_context.related_functions == []


def test_enrich_with_call_graph_boosts_neighbors(
    retriever, store, fake_embedder, monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_TOP_K_FUNCTIONS", 1)
    monkeypatch.setattr("config.settings.settings.RETRIEVER_SCORE_THRESHOLD", None)

    target = make_symbol("process", "def process(): helper()")
    helper = make_symbol("helper", "def helper(): pass")
    distant = make_symbol("distant", "def distant(): pass")

    call_graph = CallGraph(
        nodes={
            "process": CallGraphNode(
                qualified_name="process",
                calls=["helper"],
                called_by=[],
            ),
            "helper": CallGraphNode(
                qualified_name="helper",
                calls=[],
                called_by=["process"],
            ),
        }
    )

    helper_vec = [1.0] + [0.0] * (TEST_DIM - 1)
    _upsert_symbol(store, "helper", helper_vec, "def helper(): pass")
    # distant fica fora do índice vetorial para não superar o vizinho do call graph

    ctx = FunctionContext.from_symbol(target)
    enriched = retriever.enrich(
        ctx,
        target,
        call_graph=call_graph,
        symbols_by_name={
            "process": target,
            "helper": helper,
            "distant": distant,
        },
        project_root=tmp_path,
    )

    assert enriched.retrieval_context is not None
    assert enriched.retrieval_context.callee_functions == ["symbol: helper\ndef helper(): pass"]
    assert enriched.retrieval_context.related_functions == ["symbol: helper\ndef helper(): pass"]


def test_enrich_with_dependency_graph(
    retriever, store, fake_embedder, monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_SCORE_THRESHOLD", None)

    service_file = tmp_path / "app" / "service.py"
    utils_file = tmp_path / "app" / "utils.py"
    service_file.parent.mkdir(parents=True)
    service_file.write_text("pass", encoding="utf-8")
    utils_file.write_text("pass", encoding="utf-8")

    target = make_symbol("run", "def run(): pass")
    target.file_path = str(service_file)
    util_fn = make_symbol("format", "def format(): pass")
    util_fn.file_path = str(utils_file)

    dependency_graph = DependencyGraph(
        nodes={
            "app.service": DependencyNode(
                qualified_name="app.service",
                dependencies=["app.utils"],
            ),
            "app.utils": DependencyNode(
                qualified_name="app.utils",
                dependencies=[],
            ),
        }
    )

    _upsert_symbol(store, "format", [0.5] * TEST_DIM, "def format(): pass")

    ctx = FunctionContext.from_symbol(target)
    enriched = retriever.enrich(
        ctx,
        target,
        dependency_graph=dependency_graph,
        symbols_by_name={"run": target, "format": util_fn},
        project_root=tmp_path,
    )

    assert enriched.retrieval_context is not None
    assert enriched.retrieval_context.dependency_functions == ["symbol: format\ndef format(): pass"]


def test_enrich_returns_top_k(retriever, store, monkeypatch) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_TOP_K_FUNCTIONS", 3)
    monkeypatch.setattr("config.settings.settings.RETRIEVER_SCORE_THRESHOLD", None)

    target = make_symbol("target", "def target(): pass")
    _upsert_symbol(store, "target", [0.0] * TEST_DIM, "def target(): pass")

    for i in range(15):
        _upsert_symbol(store, f"fn_{i}", [float(i) / 20] * TEST_DIM, f"def fn_{i}(): pass")

    symbols_by_name = {target.qualified_name: target}
    for i in range(15):
        symbols_by_name[f"fn_{i}"] = make_symbol(f"fn_{i}", f"def fn_{i}(): pass")

    ctx = FunctionContext.from_symbol(target)
    enriched = retriever.enrich(ctx, target, symbols_by_name=symbols_by_name)

    assert enriched.retrieval_context is not None
    assert len(enriched.retrieval_context.related_functions) == 3


def test_enrich_graceful_without_collection(retriever) -> None:
    symbol = make_symbol("orphan", "def orphan(): pass")
    ctx = FunctionContext.from_symbol(symbol)
    enriched = retriever.enrich(ctx, symbol)

    assert enriched.retrieval_context is not None
    assert enriched.retrieval_context.related_functions == []
    assert enriched.retrieval_context.similar_tests == []


def test_enrich_similar_tests_from_tests_collection(
    retriever, store, fake_embedder, monkeypatch
) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_TOP_K_TESTS", 2)
    monkeypatch.setattr("config.settings.settings.RETRIEVER_SCORE_THRESHOLD", None)

    symbol = make_symbol("add", "def add(a, b): return a + b")
    store.upsert(
        "tests",
        [
            make_record(
                "test_add",
                [0.2] * TEST_DIM,
                symbol_type="test_function",
                text="def test_add(): assert add(1, 2) == 3",
            ),
            make_record(
                "test_sub",
                [0.9] * TEST_DIM,
                symbol_type="test_function",
                text="def test_sub(): assert sub(1, 2) == -1",
            ),
        ],
    )

    ctx = FunctionContext.from_symbol(symbol)
    enriched = retriever.enrich(ctx, symbol)

    assert enriched.retrieval_context is not None
    assert len(enriched.retrieval_context.similar_tests) <= 2


def test_metrics_logged(retriever, store, caplog, monkeypatch) -> None:
    monkeypatch.setattr("config.settings.settings.RETRIEVER_SCORE_THRESHOLD", None)

    symbol = make_symbol("logged", "def logged(): pass")
    _upsert_symbol(store, "logged", [0.1] * TEST_DIM, "def logged(): pass")
    _upsert_symbol(store, "other", [0.2] * TEST_DIM, "def other(): pass")

    ctx = FunctionContext.from_symbol(symbol)
    with caplog.at_level("INFO", logger="retrieval.retriever"):
        retriever.enrich(
            ctx,
            symbol,
            symbols_by_name={"logged": symbol, "other": make_symbol("other", "def other(): pass")},
        )

    assert any("retrieval[logged]" in record.message for record in caplog.records)
