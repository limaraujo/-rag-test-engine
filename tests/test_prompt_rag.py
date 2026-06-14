from __future__ import annotations

import logging

import pytest

from config.settings import settings
from schemas.context import FunctionContext
from schemas.prompt_utils import (
    RagCategory,
    RagItem,
    build_rag_prompt_sections,
    compact_rag_snippet,
    deduplicate_rag_items,
    rag_items_from_lists,
    truncate_utf8,
)
from schemas.retrieval_context import RetrievalContext


def _ctx(**kwargs) -> FunctionContext:
    base = dict(
        function_name="foo",
        qualified_name="foo",
        symbol_type="function",
        file_path="mod.py",
        code="def foo(): pass",
    )
    base.update(kwargs)
    return FunctionContext(**base)


def _large_snippet(name: str, size: int = 800) -> str:
    return f"symbol: {name}\ndef {name}():\n    {'x = 1\n    ' * (size // 10)}"


def test_same_symbol_in_caller_and_related_appears_once() -> None:
    code = "symbol: helper\ndef helper(): return 1"
    items = [
        RagItem(content=code, category=RagCategory.CALLER, qualified_name="helper"),
        RagItem(content=code, category=RagCategory.RELATED, qualified_name="helper"),
    ]
    deduped = deduplicate_rag_items(items)
    assert len(deduped) == 1
    assert deduped[0].category == RagCategory.CALLER

    ctx = _ctx(
        retrieval_context=RetrievalContext(caller_functions=[code]),
        related_functions=[code],
    )
    prompt = ctx.to_prompt_block()
    assert prompt.count("def helper(): return 1") == 1


def test_total_budget_never_exceeded() -> None:
    items = [
        RagItem(content=_large_snippet(f"fn{i}", 400), category=RagCategory.RELATED)
        for i in range(8)
    ]
    max_total = 500
    max_snippet = 200
    sections, metrics = build_rag_prompt_sections(
        items,
        max_total_chars=max_total,
        max_snippet_chars=max_snippet,
        log_metrics=False,
    )
    body_chars = metrics.chars_after
    assert body_chars <= max_total
    assert metrics.chars_before > max_total
    assert metrics.dropped_by_budget


def test_large_snippets_truncated() -> None:
    huge = "a" * 500
    compact = compact_rag_snippet(huge, max_chars=50)
    assert len(compact) <= 50
    assert compact.endswith("(truncado)")


def test_empty_context_works() -> None:
    ctx = _ctx()
    prompt = ctx.to_prompt_block()
    assert "## Função alvo" in prompt
    assert "Funções chamadoras" not in prompt

    sections, metrics = build_rag_prompt_sections(
        [],
        max_total_chars=100,
        max_snippet_chars=50,
        log_metrics=False,
    )
    assert sections == []
    assert metrics.candidates_total == 0


def test_unicode_not_split() -> None:
    text = "def f(): return '日本語🎉'"
    truncated = truncate_utf8(text, 20)
    assert truncated.encode("utf-8").decode("utf-8") == truncated
    assert "日本語" in truncated or truncated.endswith("(truncado)")


def test_priority_respected() -> None:
    shared = "symbol: shared\ndef shared(): pass"
    items = [
        RagItem(content=shared, category=RagCategory.SIMILAR_TEST, qualified_name="shared"),
        RagItem(content=shared, category=RagCategory.RELATED, qualified_name="shared"),
        RagItem(content=shared, category=RagCategory.CALLER, qualified_name="shared"),
        RagItem(content=shared, category=RagCategory.CALLEE, qualified_name="shared"),
        RagItem(content=shared, category=RagCategory.DEPENDENCY, qualified_name="shared"),
    ]
    deduped = deduplicate_rag_items(items)
    assert len(deduped) == 1
    assert deduped[0].category == RagCategory.DEPENDENCY

    sections, _ = build_rag_prompt_sections(
        items,
        max_total_chars=2500,
        max_snippet_chars=300,
        log_metrics=False,
    )
    prompt = "\n".join(sections)
    assert "## Dependências estruturais" in prompt
    assert "## Testes similares" not in prompt


def test_env_config_works(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "PROMPT_MAX_RAG_TOTAL_CHARS", 120)
    monkeypatch.setattr(settings, "PROMPT_MAX_RAG_SNIPPET_CHARS", 40)

    items = rag_items_from_lists(
        related_functions=[_large_snippet("a"), _large_snippet("b")],
    )
    sections, metrics = build_rag_prompt_sections(
        items,
        max_total_chars=settings.PROMPT_MAX_RAG_TOTAL_CHARS,
        max_snippet_chars=settings.PROMPT_MAX_RAG_SNIPPET_CHARS,
        log_metrics=False,
    )
    assert metrics.chars_after <= settings.PROMPT_MAX_RAG_TOTAL_CHARS
    assert sections


def test_rag_metrics_logged(caplog: pytest.LogCaptureFixture) -> None:
    items = [RagItem(content="symbol: x\ndef x(): pass", category=RagCategory.CALLEE)]
    with caplog.at_level(logging.INFO, logger="schemas.prompt_utils"):
        build_rag_prompt_sections(
            items,
            max_total_chars=500,
            max_snippet_chars=100,
        )
    assert any("rag_prompt candidates=" in r.message for r in caplog.records)


def test_dedup_by_code_hash_without_qname() -> None:
    code = "def anon(): return 42"
    items = [
        RagItem(content=code, category=RagCategory.CALLER),
        RagItem(content=code, category=RagCategory.RELATED),
    ]
    assert len(deduplicate_rag_items(items)) == 1


def test_retriever_defaults_in_settings() -> None:
    assert settings.RETRIEVER_TOP_K == 3
    assert settings.RETRIEVER_TOP_K_FUNCTIONS == 3
    assert settings.RETRIEVER_TOP_K_TESTS == 2
    assert settings.RETRIEVER_RERANK_POOL_SIZE == 10
    assert settings.PROMPT_MAX_RAG_TOTAL_CHARS == 2500
    assert settings.PROMPT_MAX_RAG_SNIPPET_CHARS == 300
