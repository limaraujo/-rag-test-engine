from __future__ import annotations

import json

from config.settings import settings
from llm.models import TokenUsage

# Preços por 1M tokens: {"input": float, "output": float}
_pricing_cache: dict[str, dict[str, float]] | None = None


def _load_pricing() -> dict[str, dict[str, float]]:
    global _pricing_cache
    if _pricing_cache is not None:
        return _pricing_cache

    raw = (settings.LLM_PRICING_JSON or "").strip()
    if not raw:
        _pricing_cache = {}
        return _pricing_cache

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        _pricing_cache = {}
        return _pricing_cache

    if not isinstance(data, dict):
        _pricing_cache = {}
        return _pricing_cache

    _pricing_cache = data
    return _pricing_cache


def reset_pricing_cache() -> None:
    """Limpa cache de preços (útil em testes)."""
    global _pricing_cache
    _pricing_cache = None


def pricing_configured() -> bool:
    return bool(_load_pricing())


def estimate_cost(model: str, usage: TokenUsage) -> float | None:
    """
    Estima custo em USD quando há tabela de preços configurada.

    Retorna ``None`` se não houver tabela ou modelo desconhecido.
    """
    pricing = _load_pricing()
    if not pricing:
        return None

    rates = pricing.get(model) or pricing.get("*")
    if not rates:
        return None

    input_rate = float(rates.get("input", 0))
    output_rate = float(rates.get("output", 0))

    # Desconta tokens em cache do prompt (não inventa taxa separada).
    billable_prompt = usage.prompt_tokens
    if usage.cached_prompt_tokens is not None:
        billable_prompt = max(0, usage.prompt_tokens - usage.cached_prompt_tokens)

    cost = (
        billable_prompt * input_rate / 1_000_000
        + usage.completion_tokens * output_rate / 1_000_000
    )
    return round(cost, 8)
