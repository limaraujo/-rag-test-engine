"""
Testes do cache persistente de geração de testes.

Cobre lookup, invalidação, stale, persistência, escrita atômica e integração
com o orchestrator (sem chamadas LLM em execuções idênticas).
"""
from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent
from unittest.mock import MagicMock

import pytest

from agents.orchestrator import OrchestratorAgent
from agents.policies.llm_budget import LLMBudget
from agents.services.generation_service import generate_with_cache
from agents.test_generator import TestGeneratorAgent as GeneratorAgent
from cache.generation_cache import (
    GenerationCache,
    normalize_source_code,
    source_code_hash,
)
from config.settings import ROOT, settings
from execution.runner import TestRunner
from llm.mock_llm import MockLLM
from llm.models import LLMRequest, LLMResponse
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from schemas.pipeline import GenerationCacheStats, PipelineStats
from tests.conftest import FakeEmbedder, make_symbol


class CountingLLM(MockLLM):
    """MockLLM que conta chamadas a generate()."""

    def __init__(self) -> None:
        super().__init__()
        self.generate_calls = 0

    def generate(self, request: LLMRequest) -> LLMResponse:
        self.generate_calls += 1
        return super().generate(request)


def _ctx(
    *,
    code: str = "def add(a, b):\n    return a + b",
    qname: str = "add",
) -> FunctionContext:
    return FunctionContext(
        function_name=qname.split(".")[-1],
        qualified_name=qname,
        symbol_type="function",
        file_path="tests/fixtures/cache_sample/add.py",
        module_name="tests.fixtures.cache_sample.add",
        code=code,
    )


def _passing_test(*, target: str = "add") -> GeneratedTest:
    return GeneratedTest(
        target_function=target,
        code=dedent(f"""\
            from tests.fixtures.cache_sample.add import {target}

            def test_{target}_works():
                assert {target}(1, 2) == 3
        """).strip(),
        imports=[f"from tests.fixtures.cache_sample.add import {target}"],
        coverage_hints=[],
    )


def _failing_test(*, target: str = "add") -> GeneratedTest:
    return GeneratedTest(
        target_function=target,
        code=dedent(f"""\
            from tests.fixtures.cache_sample.add import {target}

            def test_{target}_broken():
                assert {target}(1, 2) == 99
        """).strip(),
        imports=[],
        coverage_hints=[],
    )


@pytest.fixture
def cache_dir(tmp_path: Path) -> Path:
    path = tmp_path / "generation_cache"
    path.mkdir()
    return path


@pytest.fixture
def cache(cache_dir: Path, monkeypatch: pytest.MonkeyPatch) -> GenerationCache:
    monkeypatch.setattr(settings, "GENERATION_CACHE_ENABLED", True)
    monkeypatch.setattr(settings, "GENERATION_CACHE_DIR", str(cache_dir))
    monkeypatch.setattr(settings, "GENERATION_CACHE_SCHEMA_VERSION", 1)
    return GenerationCache(cache_dir=cache_dir)


@pytest.fixture
def sample_module() -> Path:
    return ROOT / "tests" / "fixtures" / "cache_sample"


# ── Unitários do módulo de cache ─────────────────────────────────────────────

def test_normalize_source_code_strips_trailing_whitespace() -> None:
    raw = "def f():\r\n    return 1  \r\n"
    assert normalize_source_code(raw) == "def f():\n    return 1"


def test_source_code_hash_changes_when_code_changes() -> None:
    h1 = source_code_hash("def add(a, b):\n    return a + b")
    h2 = source_code_hash("def add(a, b):\n    return a + b + 1")
    assert h1 != h2


def test_save_and_lookup_roundtrip(cache: GenerationCache) -> None:
    ctx = _ctx()
    test = _passing_test()
    cache.save(ctx, test, operation="generate", model="mock-offline")

    entry = cache.lookup(ctx, operation="generate", model="mock-offline")
    assert entry is not None
    materialized = cache.materialize(entry)
    assert materialized.code == test.code


def test_cache_entry_has_no_secrets(cache: GenerationCache) -> None:
    ctx = _ctx()
    test = _passing_test()
    path = cache.save(ctx, test, operation="generate", model="mock-offline")
    assert path is not None

    raw = json.loads(path.read_text(encoding="utf-8"))
    blob = json.dumps(raw).lower()
    assert "system_prompt" not in blob
    assert "user_prompt" not in blob
    assert "openai_api_key" not in blob
    assert "sk-" not in blob


def test_atomic_write_leaves_no_temp_files(cache: GenerationCache) -> None:
    ctx = _ctx()
    test = _passing_test()
    path = cache.save(ctx, test, operation="generate", model="mock-offline")
    assert path is not None
    assert path.is_file()
    assert list(path.parent.glob("*.tmp")) == []


def test_persistence_between_processes(cache_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "GENERATION_CACHE_ENABLED", True)
    monkeypatch.setattr(settings, "GENERATION_CACHE_SCHEMA_VERSION", 1)

    writer = GenerationCache(cache_dir=cache_dir)
    reader = GenerationCache(cache_dir=cache_dir)
    ctx = _ctx()
    test = _passing_test()

    writer.save(ctx, test, operation="generate", model="mock-offline")
    entry = reader.lookup(ctx, operation="generate", model="mock-offline")

    assert entry is not None
    assert reader.materialize(entry).target_function == "add"


def test_corrupt_cache_falls_back_safely(
    cache: GenerationCache,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ctx = _ctx()
    key = cache.build_cache_key(ctx, operation="generate", model="mock-offline")
    path = cache._entry_path(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not valid json", encoding="utf-8")

    entry = cache.lookup(ctx, operation="generate", model="mock-offline")
    assert entry is None


def test_schema_mismatch_invalidates_entry(cache: GenerationCache) -> None:
    ctx = _ctx()
    test = _passing_test()
    cache.save(ctx, test, operation="generate", model="mock-offline")

    key = cache.build_cache_key(ctx, operation="generate", model="mock-offline")
    path = cache._entry_path(key)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["schema_version"] = 999
    path.write_text(json.dumps(raw), encoding="utf-8")

    assert cache.lookup(ctx, operation="generate", model="mock-offline") is None


def test_mark_stale_preserves_entry(cache: GenerationCache) -> None:
    ctx = _ctx()
    test = _passing_test()
    cache.save(ctx, test, operation="generate", model="mock-offline")
    key = cache.build_cache_key(ctx, operation="generate", model="mock-offline")

    cache.mark_stale(key, reason="pytest_failed")
    path = cache._entry_path(key)
    raw = json.loads(path.read_text(encoding="utf-8"))

    assert raw["status"] == "stale"
    assert raw["stale_reason"] == "pytest_failed"
    assert raw["generated_test"]["code"] == test.code
    assert cache.lookup(ctx, operation="generate", model="mock-offline") is None


def test_prompt_version_change_causes_miss(cache: GenerationCache, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _ctx()
    test = _passing_test()
    cache.save(ctx, test, operation="generate", model="mock-offline")

    import agents.test_generator as tg

    original = tg.PROMPT_VERSION
    monkeypatch.setattr(tg, "PROMPT_VERSION", "999")
    try:
        assert cache.lookup(ctx, operation="generate", model="mock-offline") is None
    finally:
        monkeypatch.setattr(tg, "PROMPT_VERSION", original)


def test_code_change_causes_miss(cache: GenerationCache) -> None:
    ctx = _ctx()
    test = _passing_test()
    cache.save(ctx, test, operation="generate", model="mock-offline")

    changed = _ctx(code="def add(a, b):\n    return a + b + 1")
    assert cache.lookup(changed, operation="generate", model="mock-offline") is None


# ── Integração com orchestrator ────────────────────────────────────────────────

@pytest.fixture
def orchestrator_setup(
    cache_dir: Path,
    sample_module: Path,
    monkeypatch: pytest.MonkeyPatch,
    store,
    fake_embedder: FakeEmbedder,
) -> tuple[OrchestratorAgent, CountingLLM, Path]:
    monkeypatch.setattr(settings, "GENERATION_CACHE_ENABLED", True)
    monkeypatch.setattr(settings, "GENERATION_CACHE_DIR", str(cache_dir))
    monkeypatch.setattr(settings, "GENERATION_CACHE_SCHEMA_VERSION", 1)
    monkeypatch.setattr(settings, "MAX_COVERAGE_ROUNDS", 0)
    monkeypatch.setattr(settings, "MAX_REPAIRS", 0)
    monkeypatch.setattr(settings, "AI_MODE", "offline")
    monkeypatch.setattr(settings, "LOG_API_CALLS", False)

    llm = CountingLLM()
    from retrieval.retriever import Retriever

    retriever = Retriever(store=store, embedder=fake_embedder)
    retriever.index_generated_test = MagicMock(return_value=0)
    generator = GeneratorAgent(llm=llm)
    orchestrator = OrchestratorAgent(
        retriever=retriever,
        generator=generator,
        runner=TestRunner(),
        generation_cache=GenerationCache(cache_dir=cache_dir),
    )
    return orchestrator, llm, sample_module


def _run_symbol(
    orchestrator: OrchestratorAgent,
    sample_module: Path,
    stats: PipelineStats | None = None,
) -> None:
    from config.run_workspace import RunWorkspace

    add_path = str((sample_module / "add.py").resolve())
    symbol = make_symbol(
        "add",
        source_code="def add(a, b):\n    return a + b",
    ).model_copy(update={"file_path": add_path})
    workspace = RunWorkspace.create(sample_module, runs_base=ROOT / "runs" / "_test_cache")
    stats = stats or PipelineStats()

    orchestrator._process_symbol(
        symbol,
        workspace=workspace,
        call_graph=MagicMock(nodes={}),
        dependency_graph=MagicMock(nodes={}),
        symbols_by_name={symbol.qualified_name: symbol},
        source_dir=ROOT,
        pythonpath=[str(ROOT)],
        stats=stats,
    )


def test_first_run_miss_and_generation(orchestrator_setup) -> None:
    orchestrator, llm, sample_module = orchestrator_setup
    stats = PipelineStats()

    _run_symbol(orchestrator, sample_module, stats)

    assert llm.generate_calls == 1
    assert stats.generation_cache.misses == 1
    assert stats.generation_cache.hits == 0
    assert stats.ok == 1


def test_second_identical_run_cache_hit_zero_generate(orchestrator_setup) -> None:
    orchestrator, llm, sample_module = orchestrator_setup

    _run_symbol(orchestrator, sample_module)
    first_calls = llm.generate_calls
    assert first_calls >= 1

    _run_symbol(orchestrator, sample_module)
    assert llm.generate_calls == first_calls


def test_stale_cached_test_regenerates(
    cache_dir: Path,
    sample_module: Path,
    monkeypatch: pytest.MonkeyPatch,
    store,
    fake_embedder: FakeEmbedder,
) -> None:
    monkeypatch.setattr(settings, "GENERATION_CACHE_ENABLED", True)
    monkeypatch.setattr(settings, "GENERATION_CACHE_DIR", str(cache_dir))
    monkeypatch.setattr(settings, "GENERATION_CACHE_SCHEMA_VERSION", 1)
    monkeypatch.setattr(settings, "MAX_COVERAGE_ROUNDS", 0)
    monkeypatch.setattr(settings, "MAX_REPAIRS", 0)

    llm = CountingLLM()
    from retrieval.retriever import Retriever

    cache = GenerationCache(cache_dir=cache_dir)
    add_path = str((sample_module / "add.py").resolve())
    ctx = FunctionContext.from_symbol(
        make_symbol(
            "add",
            source_code="def add(a, b):\n    return a + b",
        ).model_copy(update={"file_path": add_path}),
        project_root=ROOT,
    )
    cache.save(ctx, _failing_test(), operation="generate", model="mock-offline")

    orchestrator = OrchestratorAgent(
        retriever=Retriever(store=store, embedder=fake_embedder),
        generator=GeneratorAgent(llm=llm),
        runner=TestRunner(),
        generation_cache=cache,
    )
    stats = PipelineStats()
    _run_symbol(orchestrator, sample_module, stats)

    assert stats.generation_cache.stale == 1
    assert llm.generate_calls == 1
    assert stats.ok == 1

    active_path = cache._entry_path(
        cache.build_cache_key(ctx, operation="generate", model="mock-offline")
    )
    active_raw = json.loads(active_path.read_text(encoding="utf-8"))
    assert active_raw["status"] == "active"
    assert "test_add_broken" not in active_raw["generated_test"]["code"]


def test_generate_with_cache_corrupt_counts_invalidation(
    cache: GenerationCache,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "GENERATION_CACHE_ENABLED", True)

    ctx = _ctx()
    llm = CountingLLM()
    orchestrator = OrchestratorAgent(
        generator=GeneratorAgent(llm=llm),
        generation_cache=cache,
    )
    key = cache.build_cache_key(ctx, operation="generate", model="mock-offline")
    path = cache._entry_path(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("<<<corrupt>>>", encoding="utf-8")

    stats = GenerationCacheStats()
    budget = LLMBudget(settings.MAX_LLM_CALLS_PER_SYMBOL)
    test, from_cache, _ = generate_with_cache(
        ctx,
        pythonpath=[str(ROOT)],
        cache_stats=stats,
        budget=budget,
        generator=orchestrator._generator,
        runner=orchestrator._runner,
        generation_cache=orchestrator._generation_cache,
    )

    assert not from_cache
    assert llm.generate_calls == 1
    assert stats.invalidations == 1
    assert stats.misses == 1
    assert test.target_function == ctx.qualified_name
