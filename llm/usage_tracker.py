from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from llm.models import TokenUsage
from llm.pricing import pricing_configured
from llm.token_usage import normalize_operation, parse_label

PHASES = ("generate", "repair", "coverage", "embedding", "cache_validation")


@dataclass
class UsageBucket:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    reasoning_tokens: int = 0
    cached_prompt_tokens: int = 0
    estimated_cost: float = 0.0
    calls: int = 0
    _has_reasoning: bool = False
    _has_cached: bool = False
    _has_cost: bool = False

    def add(self, usage: TokenUsage) -> None:
        self.prompt_tokens += usage.prompt_tokens
        self.completion_tokens += usage.completion_tokens
        self.total_tokens += usage.total_tokens
        self.calls += 1

        if usage.reasoning_tokens is not None:
            self.reasoning_tokens += usage.reasoning_tokens
            self._has_reasoning = True
        if usage.cached_prompt_tokens is not None:
            self.cached_prompt_tokens += usage.cached_prompt_tokens
            self._has_cached = True
        if usage.estimated_cost is not None:
            self.estimated_cost += usage.estimated_cost
            self._has_cost = True

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "calls": self.calls,
        }
        if self.calls:
            payload["avg_per_call"] = {
                "prompt_tokens": round(self.prompt_tokens / self.calls, 2),
                "completion_tokens": round(self.completion_tokens / self.calls, 2),
                "total_tokens": round(self.total_tokens / self.calls, 2),
            }
        if self._has_reasoning:
            payload["reasoning_tokens"] = self.reasoning_tokens
            if self.calls:
                payload["avg_per_call"]["reasoning_tokens"] = round(
                    self.reasoning_tokens / self.calls, 2
                )
        if self._has_cached:
            payload["cached_prompt_tokens"] = self.cached_prompt_tokens
            if self.calls:
                payload["avg_per_call"]["cached_prompt_tokens"] = round(
                    self.cached_prompt_tokens / self.calls, 2
                )
        if self._has_cost and pricing_configured():
            payload["estimated_cost"] = round(self.estimated_cost, 8)
            if self.calls:
                payload["avg_per_call"]["estimated_cost"] = round(
                    self.estimated_cost / self.calls, 8
                )
        return payload


@dataclass
class UsageTracker:
    by_phase: dict[str, UsageBucket] = field(default_factory=dict)
    by_symbol: dict[str, UsageBucket] = field(default_factory=dict)
    by_agent: dict[str, UsageBucket] = field(default_factory=dict)
    by_operation: dict[str, UsageBucket] = field(default_factory=dict)
    by_model: dict[str, UsageBucket] = field(default_factory=dict)

    def _bucket(self, store: dict[str, UsageBucket], key: str) -> UsageBucket:
        if key not in store:
            store[key] = UsageBucket()
        return store[key]

    def record(
        self,
        usage: TokenUsage | None,
        *,
        agent: str | None = None,
        operation: str | None = None,
        symbol: str | None = None,
        model: str,
        label: str | None = None,
    ) -> None:
        if not usage:
            return

        parsed_symbol, parsed_operation = parse_label(label)
        symbol = symbol or parsed_symbol
        operation = operation or parsed_operation or "generate"
        phase = normalize_operation(operation)
        agent_key = agent or "unknown"

        self._bucket(self.by_phase, phase).add(usage)
        self._bucket(self.by_operation, operation).add(usage)
        self._bucket(self.by_agent, agent_key).add(usage)
        self._bucket(self.by_model, model).add(usage)
        if symbol:
            self._bucket(self.by_symbol, symbol).add(usage)

    def record_llm(
        self,
        usage: TokenUsage | None,
        *,
        agent: str | None = None,
        operation: str | None = None,
        symbol: str | None = None,
        model: str,
        label: str | None = None,
    ) -> None:
        self.record(
            usage,
            agent=agent,
            operation=operation,
            symbol=symbol,
            model=model,
            label=label,
        )

    def record_embedding(
        self,
        usage: TokenUsage | None,
        *,
        model: str,
        label: str | None = None,
        symbol: str | None = None,
    ) -> None:
        self.record(
            usage,
            agent="embedding",
            operation="embedding",
            symbol=symbol or label,
            model=model,
            label=label,
        )

    def reset(self) -> None:
        self.by_phase.clear()
        self.by_symbol.clear()
        self.by_agent.clear()
        self.by_operation.clear()
        self.by_model.clear()

    def totals(self) -> UsageBucket:
        total = UsageBucket()
        for bucket in self.by_phase.values():
            total.prompt_tokens += bucket.prompt_tokens
            total.completion_tokens += bucket.completion_tokens
            total.total_tokens += bucket.total_tokens
            total.calls += bucket.calls
            if bucket._has_reasoning:
                total.reasoning_tokens += bucket.reasoning_tokens
                total._has_reasoning = True
            if bucket._has_cached:
                total.cached_prompt_tokens += bucket.cached_prompt_tokens
                total._has_cached = True
            if bucket._has_cost:
                total.estimated_cost += bucket.estimated_cost
                total._has_cost = True
        return total

    def _sum_buckets(self, store: dict[str, UsageBucket]) -> UsageBucket:
        total = UsageBucket()
        for bucket in store.values():
            total.prompt_tokens += bucket.prompt_tokens
            total.completion_tokens += bucket.completion_tokens
            total.total_tokens += bucket.total_tokens
            total.calls += bucket.calls
            if bucket._has_reasoning:
                total.reasoning_tokens += bucket.reasoning_tokens
                total._has_reasoning = True
            if bucket._has_cached:
                total.cached_prompt_tokens += bucket.cached_prompt_tokens
                total._has_cached = True
            if bucket._has_cost:
                total.estimated_cost += bucket.estimated_cost
                total._has_cost = True
        return total

    def reconciliation(self) -> dict[str, Any]:
        """Verifica se agregações por fase/operação batem com o total."""
        totals = self.totals()
        by_phase = self._sum_buckets(self.by_phase)
        by_operation = self._sum_buckets(self.by_operation)
        consistent = (
            totals.total_tokens == by_phase.total_tokens == by_operation.total_tokens
            and totals.calls == by_phase.calls == by_operation.calls
        )
        return {
            "consistent": consistent,
            "totals": totals.to_dict(),
            "by_phase_sum": by_phase.to_dict(),
            "by_operation_sum": by_operation.to_dict(),
        }

    def build_summary(
        self,
        *,
        embedding_cache_hits: int = 0,
        generation_cache_hits: int = 0,
        llm_calls_avoided: int = 0,
        ignored_symbols: list[dict[str, Any]] | None = None,
        api_calls_log_totals: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        totals = self.totals()
        summary: dict[str, Any] = {
            "by_phase": {phase: self.by_phase[phase].to_dict() for phase in PHASES if phase in self.by_phase},
            "by_symbol": {key: bucket.to_dict() for key, bucket in sorted(self.by_symbol.items())},
            "by_operation": {key: bucket.to_dict() for key, bucket in sorted(self.by_operation.items())},
            "by_agent": {key: bucket.to_dict() for key, bucket in sorted(self.by_agent.items())},
            "by_model": {key: bucket.to_dict() for key, bucket in sorted(self.by_model.items())},
            "totals": totals.to_dict(),
            "reconciliation": self.reconciliation(),
            "cache": {
                "embedding_hits": embedding_cache_hits,
                "generation_hits": generation_cache_hits,
                "llm_calls_avoided": llm_calls_avoided,
            },
        }
        if api_calls_log_totals is not None:
            summary["api_calls_log_totals"] = api_calls_log_totals
            tracker_calls = totals.calls
            log_calls = int(api_calls_log_totals.get("calls", 0))
            tracker_total = totals.total_tokens
            log_total = int(api_calls_log_totals.get("total_tokens", 0))
            summary["api_calls_log_match"] = (
                tracker_calls == log_calls and tracker_total == log_total
            )
        if ignored_symbols:
            summary["ignored_symbols"] = ignored_symbols
        return summary

    def format_summary(self) -> str:
        lines: list[str] = []
        totals = self.totals()
        lines.append(f"  Total ({totals.calls} chamadas)")
        lines.append(f"    entrada  : {totals.prompt_tokens:,} tokens")
        lines.append(f"    saída    : {totals.completion_tokens:,} tokens")
        lines.append(f"    total    : {totals.total_tokens:,} tokens")
        if totals._has_reasoning:
            lines.append(f"    raciocínio: {totals.reasoning_tokens:,} tokens")
        if totals._has_cached:
            lines.append(f"    cache prompt: {totals.cached_prompt_tokens:,} tokens")
        if totals._has_cost and pricing_configured():
            lines.append(f"    custo est.: ${totals.estimated_cost:.6f}")

        for phase in PHASES:
            bucket = self.by_phase.get(phase)
            if not bucket or not bucket.calls:
                continue
            lines.append(f"  {phase} ({bucket.calls} chamadas, {bucket.total_tokens:,} tokens)")
        return "\n".join(lines)


_tracker = UsageTracker()


def get_tracker() -> UsageTracker:
    return _tracker


def reset_tracker() -> None:
    _tracker.reset()
