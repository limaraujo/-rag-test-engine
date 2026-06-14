from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from llm.models import LLMEmbeddingRequest, LLMEmbeddingResponse, LLMRequest, LLMResponse, TokenUsage

_SAFE_NAME = re.compile(r"[^a-zA-Z0-9_.-]+")


class APICallLogger:
    """Persiste entrada/saída e tokens de cada chamada à API (LLM ou embedding)."""

    def __init__(self) -> None:
        self._log_dir: Path | None = None
        self._seq = 0

    def configure(self, log_dir: Path | None) -> None:
        if log_dir is None:
            self._log_dir = None
            return
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)

    def reset(self) -> None:
        self._seq = 0

    @property
    def enabled(self) -> bool:
        return self._log_dir is not None

    def log_llm(
        self,
        request: LLMRequest,
        response: LLMResponse,
        *,
        model: str,
    ) -> Path | None:
        payload: dict[str, Any] = {
            "type": "llm",
            "agent": request.agent,
            "label": request.label,
            "model": model,
            "input": {
                "system_prompt": request.system_prompt,
                "user_prompt": request.user_prompt,
                "temperature": request.temperature,
            },
            "output": {
                "content": response.content,
            },
            "usage": _usage_dict(response.usage),
        }
        slug = _slug(request.agent, request.label, "llm")
        return self._write(payload, slug)

    def log_embedding(
        self,
        request: LLMEmbeddingRequest,
        response: LLMEmbeddingResponse,
        *,
        model: str,
    ) -> Path | None:
        payload: dict[str, Any] = {
            "type": "embedding",
            "label": request.label,
            "model": model,
            "input": {
                "text": request.input,
            },
            "output": {
                "dimensions": response.dimensions,
            },
            "usage": _usage_dict(response.usage),
        }
        slug = _slug(None, request.label, "embedding")
        return self._write(payload, slug)

    def _write(self, payload: dict[str, Any], slug: str) -> Path | None:
        if self._log_dir is None:
            return None

        self._seq += 1
        payload["seq"] = self._seq
        payload["timestamp"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

        filename = f"{self._seq:04d}_{slug}.json"
        path = self._log_dir / filename
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        index_line = {
            "seq": self._seq,
            "timestamp": payload["timestamp"],
            "type": payload["type"],
            "agent": payload.get("agent"),
            "label": payload.get("label"),
            "model": payload["model"],
            "usage": payload["usage"],
            "file": filename,
        }
        with (self._log_dir / "_index.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(index_line, ensure_ascii=False) + "\n")

        return path


def _usage_dict(usage: TokenUsage | None) -> dict[str, int] | None:
    if usage is None:
        return None
    return usage.model_dump()


def _slug(agent: str | None, label: str | None, call_type: str) -> str:
    parts = [call_type]
    if agent:
        parts.append(agent)
    if label:
        parts.append(label)
    raw = "__".join(parts)
    return _SAFE_NAME.sub("_", raw)[:120] or call_type


_logger = APICallLogger()


def get_call_logger() -> APICallLogger:
    return _logger


def configure_call_logger(log_dir: Path | None) -> None:
    _logger.configure(log_dir)


def reset_call_logger() -> None:
    _logger.reset()


def setup_api_call_logging(log_dir: Path) -> Path | None:
    """
    Ativa gravação de entradas/saídas se ``LOG_API_CALLS=true`` no ``.env``.

    Retorna o diretório de log ou ``None`` quando desativado.
    """
    from config.settings import settings

    if not settings.LOG_API_CALLS:
        configure_call_logger(None)
        return None

    configure_call_logger(log_dir)
    reset_call_logger()
    return log_dir
