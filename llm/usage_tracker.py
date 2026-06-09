from __future__ import annotations

from dataclasses import dataclass, field

from llm.models import TokenUsage


@dataclass
class UsageBucket:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    calls: int = 0

    def add(self, usage: TokenUsage) -> None:
        self.prompt_tokens += usage.prompt_tokens
        self.completion_tokens += usage.completion_tokens
        self.total_tokens += usage.total_tokens
        self.calls += 1


@dataclass
class UsageTracker:
    llm: UsageBucket = field(default_factory=UsageBucket)
    embedding: UsageBucket = field(default_factory=UsageBucket)

    def record_llm(self, usage: TokenUsage | None) -> None:
        if usage:
            self.llm.add(usage)

    def record_embedding(self, usage: TokenUsage | None) -> None:
        if usage:
            self.embedding.add(usage)

    def reset(self) -> None:
        self.llm = UsageBucket()
        self.embedding = UsageBucket()

    def format_summary(self) -> str:
        lines = [
            f"  LLM ({self.llm.calls} chamadas)",
            f"    entrada  : {self.llm.prompt_tokens:,} tokens",
            f"    saída    : {self.llm.completion_tokens:,} tokens",
            f"    total    : {self.llm.total_tokens:,} tokens",
            f"  Embeddings ({self.embedding.calls} chamadas)",
            f"    entrada  : {self.embedding.prompt_tokens:,} tokens",
            f"    total    : {self.embedding.total_tokens:,} tokens",
            (
                f"  Geral    : "
                f"{self.llm.total_tokens + self.embedding.total_tokens:,} tokens"
            ),
        ]
        return "\n".join(lines)


_tracker = UsageTracker()


def get_tracker() -> UsageTracker:
    return _tracker


def reset_tracker() -> None:
    _tracker.reset()
