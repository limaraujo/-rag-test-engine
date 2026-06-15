from __future__ import annotations

from typing import Any

from llm.models import TokenUsage
from llm.pricing import estimate_cost


def parse_label(label: str | None) -> tuple[str | None, str | None]:
    """
    Extrai ``(symbol, operation)`` de rótulos como ``pkg.func::generate``.

    Retorna ``(None, None)`` quando o rótulo não segue o formato.
    """
    if not label or "::" not in label:
        return None, label
    symbol, operation = label.rsplit("::", 1)
    return symbol or None, operation or None


def normalize_operation(operation: str | None) -> str:
    """Mapeia identificadores de operação para fases canônicas."""
    if not operation:
        return "generate"
    if operation == "embedding":
        return "embedding"
    if operation == "cache_validation":
        return "cache_validation"
    if operation.startswith("coverage"):
        return "coverage"
    if operation.startswith("repair"):
        return "repair"
    if operation == "generate":
        return "generate"
    return operation


def token_usage_from_openai(usage_obj: Any, *, model: str) -> TokenUsage | None:
    """
    Constrói :class:`TokenUsage` a partir da resposta OpenAI.

    Campos opcionais só são preenchidos quando a API os retorna.
    """
    if usage_obj is None:
        return None

    reasoning_tokens: int | None = None
    cached_prompt_tokens: int | None = None

    completion_details = getattr(usage_obj, "completion_tokens_details", None)
    if completion_details is not None:
        rt = getattr(completion_details, "reasoning_tokens", None)
        if rt is not None:
            reasoning_tokens = int(rt)

    prompt_details = getattr(usage_obj, "prompt_tokens_details", None)
    if prompt_details is not None:
        ct = getattr(prompt_details, "cached_tokens", None)
        if ct is not None:
            cached_prompt_tokens = int(ct)

    # Embeddings retornam só prompt_tokens/total_tokens (sem completion_tokens).
    prompt_tokens = int(getattr(usage_obj, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage_obj, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage_obj, "total_tokens", 0) or 0)
    if total_tokens == 0 and prompt_tokens:
        total_tokens = prompt_tokens + completion_tokens

    usage = TokenUsage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        reasoning_tokens=reasoning_tokens,
        cached_prompt_tokens=cached_prompt_tokens,
    )

    cost = estimate_cost(model, usage)
    if cost is not None:
        usage.estimated_cost = cost

    return usage


def usage_from_dict(data: dict[str, Any] | None) -> TokenUsage | None:
    """Reconstrói uso a partir de log antigo ou parcial (campos ausentes ok)."""
    if not data:
        return None
    return TokenUsage(
        prompt_tokens=int(data.get("prompt_tokens", 0)),
        completion_tokens=int(data.get("completion_tokens", 0)),
        total_tokens=int(data.get("total_tokens", 0)),
        reasoning_tokens=data.get("reasoning_tokens"),
        cached_prompt_tokens=data.get("cached_prompt_tokens"),
        estimated_cost=data.get("estimated_cost"),
    )
