from __future__ import annotations

import json
from pathlib import Path

import pytest

from llm.call_logger import APICallLogger, configure_call_logger, reset_call_logger, setup_api_call_logging
from llm.models import LLMEmbeddingRequest, LLMEmbeddingResponse, LLMRequest, LLMResponse, TokenUsage


@pytest.fixture(autouse=True)
def _enable_bodies_for_legacy_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    from config import settings as settings_module

    monkeypatch.setattr(settings_module.settings, "LOG_API_CALL_BODIES", True)
    monkeypatch.setattr(settings_module.settings, "LOG_API_CALL_METADATA", True)


def test_log_llm_writes_input_output_and_usage(tmp_path: Path) -> None:
    configure_call_logger(tmp_path)
    reset_call_logger()

    logger = APICallLogger()
    logger.configure(tmp_path)
    logger.reset()

    request = LLMRequest(
        system_prompt="system",
        user_prompt="user context",
        temperature=0.1,
        agent="test_generator",
        label="module.func::generate",
        operation="generate",
        symbol="module.func",
    )
    response = LLMResponse(
        content="def test_foo(): pass",
        model="mock",
        usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )

    path = logger.log_llm(request, response, model="mock")
    assert path is not None
    assert path.exists()

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["type"] == "llm"
    assert payload["agent"] == "test_generator"
    assert payload["operation"] == "generate"
    assert payload["symbol"] == "module.func"
    assert payload["input"]["user_prompt"] == "user context"
    assert payload["output"]["content"].startswith("def test_foo")
    assert payload["usage"]["total_tokens"] == 15
    assert payload["metadata"]["user_prompt_chars"] == len("user context")

    index_lines = (tmp_path / "_index.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(index_lines) == 1
    index = json.loads(index_lines[0])
    assert index["seq"] == 1
    assert index["usage"]["total_tokens"] == 15
    assert index["operation"] == "generate"


def test_log_embedding_writes_text_input(tmp_path: Path) -> None:
    configure_call_logger(tmp_path)
    reset_call_logger()

    logger = APICallLogger()
    logger.configure(tmp_path)
    logger.reset()

    request = LLMEmbeddingRequest(
        input="symbol: pkg.func\ncode:\ndef func(): pass",
        model="text-embedding-3-small",
        label="pkg.func",
        symbol="pkg.func",
    )
    response = LLMEmbeddingResponse(
        embedding=[0.1, 0.2],
        model="text-embedding-3-small",
        dimensions=2,
        usage=TokenUsage(prompt_tokens=42, completion_tokens=0, total_tokens=42),
    )

    path = logger.log_embedding(request, response, model="text-embedding-3-small")
    assert path is not None

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["type"] == "embedding"
    assert payload["label"] == "pkg.func"
    assert payload["operation"] == "embedding"
    assert "pkg.func" in payload["input"]["text"]
    assert payload["usage"]["prompt_tokens"] == 42


def test_setup_api_call_logging_respects_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from config import settings as settings_module

    monkeypatch.setattr(settings_module.settings, "LOG_API_CALLS", True)
    active = setup_api_call_logging(tmp_path)
    assert active == tmp_path
    assert tmp_path.exists()

    monkeypatch.setattr(settings_module.settings, "LOG_API_CALLS", False)
    assert setup_api_call_logging(tmp_path / "ignored") is None


def test_logger_disabled_when_not_configured() -> None:
    configure_call_logger(None)
    reset_call_logger()

    logger = APICallLogger()
    request = LLMRequest(system_prompt="s", user_prompt="u")
    response = LLMResponse(content="ok", model="mock")

    assert logger.log_llm(request, response, model="mock") is None
