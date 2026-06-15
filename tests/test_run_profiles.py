from __future__ import annotations

import pytest

from config.run_profiles import PROFILES, apply_run_profile, get_active_profile
from config.settings import settings


def test_profile_choices_cover_four_modes() -> None:
    assert set(PROFILES) == {"sem-rag", "rag-limitado", "rag-completo", "com-cache"}


def test_sem_rag_profile_disables_rag_and_cache() -> None:
    original_rag = settings.RAG_MODE
    original_cache = settings.GENERATION_CACHE_ENABLED
    with apply_run_profile("sem-rag"):
        assert settings.RAG_MODE == "none"
        assert settings.GENERATION_CACHE_ENABLED is False
        assert get_active_profile() is not None
        assert get_active_profile().name == "sem-rag"
    assert settings.RAG_MODE == original_rag
    assert settings.GENERATION_CACHE_ENABLED == original_cache
    assert get_active_profile() is None


def test_rag_limitado_applies_budget_overrides() -> None:
    with apply_run_profile("rag-limitado"):
        assert settings.RAG_MODE == "limited"
        assert settings.GENERATION_CACHE_ENABLED is False
        assert settings.PROMPT_MAX_RAG_TOTAL_CHARS == 600
        assert settings.RETRIEVER_TOP_K_FUNCTIONS == 1


def test_rag_completo_disables_cache() -> None:
    with apply_run_profile("rag-completo"):
        assert settings.RAG_MODE == "full"
        assert settings.GENERATION_CACHE_ENABLED is False


def test_com_cache_enables_generation_cache() -> None:
    with apply_run_profile("com-cache"):
        assert settings.RAG_MODE == "full"
        assert settings.GENERATION_CACHE_ENABLED is True


def test_orchestrator_skips_index_when_rag_none(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    from agents.orchestrator import OrchestratorAgent
    from tests.conftest import make_symbol

    monkeypatch.setattr(settings, "RAG_MODE", "none")
    monkeypatch.setattr(settings, "AI_MODE", "offline")
    monkeypatch.setattr(settings, "LOG_API_CALLS", False)
    monkeypatch.setattr(settings, "GENERATION_CACHE_ENABLED", False)
    monkeypatch.setattr(settings, "MAX_COVERAGE_ROUNDS", 0)
    monkeypatch.setattr(settings, "MAX_REPAIRS", 0)

    sample = tmp_path / "sample.py"
    sample.write_text(
        "def add(a, b):\n    return a + b\n",
        encoding="utf-8",
    )

    agent = OrchestratorAgent()
    indexed, cache_hits = agent._index([
        make_symbol("add", source_code="def add(a, b):\n    return a + b\n"),
    ])
    assert indexed == 0
    assert cache_hits == 0
