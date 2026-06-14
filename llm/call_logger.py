from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config.settings import settings
from llm.models import LLMEmbeddingRequest, LLMEmbeddingResponse, LLMRequest, LLMResponse, TokenUsage
from llm.sanitize import sanitize_text
from llm.token_usage import parse_label, usage_from_dict

_SAFE_NAME = re.compile(r"[^a-zA-Z0-9_.-]+")


class APICallLogger:
    """Persiste metadados e, opcionalmente, corpos de chamadas LLM/embedding."""

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
        symbol, operation = _resolve_context(request)
        payload: dict[str, Any] = {
            "type": "llm",
            "agent": request.agent,
            "operation": operation,
            "symbol": symbol,
            "label": request.label,
            "model": model,
            "usage": _usage_dict(response.usage),
        }
        if settings.LOG_API_CALL_METADATA:
            payload["metadata"] = {
                "system_prompt_chars": len(request.system_prompt),
                "user_prompt_chars": len(request.user_prompt),
                "output_chars": len(response.content),
                "temperature": request.temperature,
            }
        if settings.LOG_API_CALL_BODIES:
            payload["input"] = {
                "system_prompt": sanitize_text(request.system_prompt),
                "user_prompt": sanitize_text(request.user_prompt),
                "temperature": request.temperature,
            }
            payload["output"] = {
                "content": sanitize_text(response.content),
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
        symbol = request.symbol or request.label
        payload: dict[str, Any] = {
            "type": "embedding",
            "operation": request.operation or "embedding",
            "symbol": symbol,
            "label": request.label,
            "model": model,
            "usage": _usage_dict(response.usage),
        }
        if settings.LOG_API_CALL_METADATA:
            payload["metadata"] = {
                "input_chars": len(request.input),
                "dimensions": response.dimensions,
            }
        if settings.LOG_API_CALL_BODIES:
            payload["input"] = {
                "text": sanitize_text(request.input),
            }
            payload["output"] = {
                "dimensions": response.dimensions,
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
            "operation": payload.get("operation"),
            "symbol": payload.get("symbol"),
            "label": payload.get("label"),
            "model": payload["model"],
            "usage": payload["usage"],
            "file": filename,
        }
        with (self._log_dir / "_index.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(index_line, ensure_ascii=False) + "\n")

        return path


def _resolve_context(request: LLMRequest) -> tuple[str | None, str | None]:
    symbol = request.symbol
    operation = request.operation
    if symbol is None or operation is None:
        parsed_symbol, parsed_operation = parse_label(request.label)
        symbol = symbol or parsed_symbol
        operation = operation or parsed_operation
    return symbol, operation


def _usage_dict(usage: TokenUsage | None) -> dict[str, int | float] | None:
    if usage is None:
        return None
    data = usage.model_dump(exclude_none=True)
    return data or None


def load_call_log(path: Path) -> dict[str, Any]:
    """
    Carrega um log de chamada, compatível com formato antigo e novo.

    Campos ausentes não causam erro.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["usage"] = usage_from_dict(payload.get("usage"))
    return payload


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
    Ativa gravação de chamadas se ``LOG_API_CALLS=true`` no ``.env``.

    Retorna o diretório de log ou ``None`` quando desativado.
    """
    if not settings.LOG_API_CALLS:
        configure_call_logger(None)
        return None

    configure_call_logger(log_dir)
    reset_call_logger()
    return log_dir
