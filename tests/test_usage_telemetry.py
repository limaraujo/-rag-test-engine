from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from config.run_workspace import RunWorkspace, save_run_summary
from llm.call_logger import APICallLogger, configure_call_logger, load_call_log, reset_call_logger
from llm.models import LLMRequest, LLMResponse, TokenUsage
from llm.pricing import reset_pricing_cache
from llm.sanitize import sanitize_text
from llm.token_usage import token_usage_from_openai, usage_from_dict
from llm.usage_tracker import UsageTracker, get_tracker, reset_tracker


@pytest.fixture(autouse=True)
def _reset_globals() -> None:
    reset_tracker()
    reset_pricing_cache()
    configure_call_logger(None)
    reset_call_logger()


def _openai_usage(
    *,
    prompt: int = 100,
    completion: int = 50,
    total: int = 150,
    reasoning: int | None = None,
    cached: int | None = None,
) -> SimpleNamespace:
    completion_details = None
    if reasoning is not None:
        completion_details = SimpleNamespace(reasoning_tokens=reasoning)

    prompt_details = None
    if cached is not None:
        prompt_details = SimpleNamespace(cached_tokens=cached)

    return SimpleNamespace(
        prompt_tokens=prompt,
        completion_tokens=completion,
        total_tokens=total,
        completion_tokens_details=completion_details,
        prompt_tokens_details=prompt_details,
    )


def test_token_usage_from_embedding_usage() -> None:
    """API de embeddings não expõe completion_tokens."""
    usage = token_usage_from_openai(
        SimpleNamespace(prompt_tokens=42, total_tokens=42),
        model="text-embedding-3-small",
    )
    assert usage is not None
    assert usage.prompt_tokens == 42
    assert usage.completion_tokens == 0
    assert usage.total_tokens == 42


def test_token_usage_without_reasoning_tokens() -> None:
    usage = token_usage_from_openai(_openai_usage(), model="gpt-5-nano")
    assert usage is not None
    assert usage.prompt_tokens == 100
    assert usage.completion_tokens == 50
    assert usage.total_tokens == 150
    assert usage.reasoning_tokens is None
    assert usage.cached_prompt_tokens is None
    assert usage.estimated_cost is None


def test_token_usage_with_reasoning_tokens() -> None:
    usage = token_usage_from_openai(
        _openai_usage(reasoning=32),
        model="gpt-5-nano",
    )
    assert usage is not None
    assert usage.reasoning_tokens == 32
    assert usage.cached_prompt_tokens is None


def test_token_usage_with_cached_prompt_tokens_optional() -> None:
    usage = token_usage_from_openai(
        _openai_usage(cached=40),
        model="gpt-5-nano",
    )
    assert usage is not None
    assert usage.cached_prompt_tokens == 40
    assert usage.reasoning_tokens is None


def test_usage_aggregation_by_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from config import settings as settings_module

    monkeypatch.setattr(settings_module.settings, "LLM_PRICING_JSON", "")

    tracker = UsageTracker()
    tracker.record_llm(
        TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        agent="test_generator",
        operation="generate",
        symbol="pkg.add",
        model="mock",
        label="pkg.add::generate",
    )
    tracker.record_llm(
        TokenUsage(prompt_tokens=20, completion_tokens=8, total_tokens=28),
        agent="repair",
        operation="repair_1",
        symbol="pkg.add",
        model="mock",
        label="pkg.add::repair_1",
    )
    tracker.record_llm(
        TokenUsage(prompt_tokens=15, completion_tokens=6, total_tokens=21),
        agent="test_generator",
        operation="coverage_1",
        symbol="pkg.sub",
        model="mock",
        label="pkg.sub::coverage_1",
    )

    summary = tracker.build_summary()
    assert summary["by_phase"]["generate"]["calls"] == 1
    assert summary["by_phase"]["repair"]["calls"] == 1
    assert summary["by_phase"]["coverage"]["calls"] == 1
    assert summary["by_operation"]["repair_1"]["total_tokens"] == 28
    assert summary["by_symbol"]["pkg.add"]["calls"] == 2
    assert summary["by_agent"]["repair"]["calls"] == 1
    assert summary["by_model"]["mock"]["calls"] == 3
    assert summary["totals"]["calls"] == 3
    assert summary["totals"]["avg_per_call"]["total_tokens"] == round(64 / 3, 2)


def test_load_old_call_log_format(tmp_path: Path) -> None:
    old_payload = {
        "type": "llm",
        "agent": "test_generator",
        "label": "pkg.func::generate",
        "model": "mock",
        "input": {"system_prompt": "s", "user_prompt": "u", "temperature": 0.1},
        "output": {"content": "code"},
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        "seq": 1,
        "timestamp": "2026-01-01T00:00:00+00:00",
    }
    path = tmp_path / "0001_old.json"
    path.write_text(json.dumps(old_payload), encoding="utf-8")

    loaded = load_call_log(path)
    assert loaded["agent"] == "test_generator"
    assert loaded["usage"].prompt_tokens == 10
    assert loaded["usage"].reasoning_tokens is None

    usage = usage_from_dict(old_payload["usage"])
    assert usage is not None
    assert usage.total_tokens == 15


def test_call_logger_bodies_disabled_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from config import settings as settings_module

    monkeypatch.setattr(settings_module.settings, "LOG_API_CALL_BODIES", False)
    monkeypatch.setattr(settings_module.settings, "LOG_API_CALL_METADATA", True)

    logger = APICallLogger()
    logger.configure(tmp_path)
    logger.reset()

    request = LLMRequest(
        system_prompt="system secret sk-abcdefghijklmnopqrstuvwxyz",
        user_prompt="user",
        agent="test_generator",
        label="pkg.func::generate",
        operation="generate",
        symbol="pkg.func",
    )
    response = LLMResponse(
        content="def test_x(): pass",
        model="mock",
        usage=TokenUsage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
    )

    path = logger.log_llm(request, response, model="mock")
    assert path is not None
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert "input" not in payload
    assert "output" not in payload
    assert payload["metadata"]["user_prompt_chars"] == 4
    assert payload["operation"] == "generate"
    assert payload["symbol"] == "pkg.func"


def test_call_logger_bodies_enabled_when_configured(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from config import settings as settings_module

    monkeypatch.setattr(settings_module.settings, "LOG_API_CALL_BODIES", True)

    logger = APICallLogger()
    logger.configure(tmp_path)
    logger.reset()

    secret = "sk-abcdefghijklmnopqrstuvwxyz1234567890"
    request = LLMRequest(system_prompt="s", user_prompt=secret, agent="repair")
    response = LLMResponse(content="ok", model="mock")

    logger.log_llm(request, response, model="mock")
    payload = json.loads(next(tmp_path.glob("*.json")).read_text(encoding="utf-8"))
    assert secret not in json.dumps(payload)
    assert "sk-***" in payload["input"]["user_prompt"]


def test_sanitize_secret_patterns() -> None:
    raw = "OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz"
    cleaned = sanitize_text(raw)
    assert "sk-proj" not in cleaned
    assert "OPENAI_API_KEY=***" in cleaned or "sk-***" in cleaned


def test_run_summary_contains_separate_cache_hits(tmp_path: Path) -> None:
    workspace = RunWorkspace(
        root=tmp_path,
        source_dir=tmp_path / "src",
        tests_dir=tmp_path / "tests",
        logs_dir=tmp_path / "logs",
        artifacts_dir=tmp_path / "artifacts",
    )
    workspace.artifacts_dir.mkdir(parents=True, exist_ok=True)

    token_usage = get_tracker().build_summary(
        embedding_cache_hits=7,
        generation_cache_hits=3,
        llm_calls_avoided=3,
        ignored_symbols=[{"qualified_name": "main", "reason": "filtered"}],
    )

    save_run_summary(
        workspace,
        stats={
            "ok": 1,
            "embedding_cache_hits": 7,
            "generation_cache": {"hits": 3, "llm_calls_avoided": 3},
        },
        token_usage=token_usage,
    )

    summary = json.loads((workspace.artifacts_dir / "run_summary.json").read_text())
    assert summary["token_usage"]["cache"]["embedding_hits"] == 7
    assert summary["token_usage"]["cache"]["generation_hits"] == 3
    assert summary["token_usage"]["cache"]["llm_calls_avoided"] == 3
    assert summary["stats"]["embedding_cache_hits"] == 7


def test_estimated_cost_only_with_pricing_table(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from config import settings as settings_module

    reset_pricing_cache()
    monkeypatch.setattr(
        settings_module.settings,
        "LLM_PRICING_JSON",
        '{"gpt-5-nano":{"input":1.0,"output":2.0}}',
    )

    usage = token_usage_from_openai(_openai_usage(prompt=1_000_000, completion=0), model="gpt-5-nano")
    assert usage is not None
    assert usage.estimated_cost == 1.0

    monkeypatch.setattr(settings_module.settings, "LLM_PRICING_JSON", "")
    reset_pricing_cache()
    usage_no_price = token_usage_from_openai(_openai_usage(), model="gpt-5-nano")
    assert usage_no_price is not None
    assert usage_no_price.estimated_cost is None
