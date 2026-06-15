from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from config.settings import settings
from execution.runner import RunResult


class LLMBudgetExhausted(RuntimeError):
    """Orçamento de chamadas LLM por símbolo esgotado."""


@dataclass
class LLMBudget:
    max_calls: int
    calls: int = 0
    operations: list[str] = field(default_factory=list)

    def can_call(self) -> bool:
        return self.calls < self.max_calls

    def record(self, operation: str) -> bool:
        if not self.can_call():
            return False
        self.calls += 1
        self.operations.append(operation)
        return True


# Alias legado usado em testes e código interno.
_LLMBudget = LLMBudget


def error_fingerprint(result: RunResult) -> str:
    """Hash estável do erro de pytest para detectar repetição no loop de reparo."""
    text = (result.failure_summary or result.output).strip()
    text = re.sub(r"C:\\Users\\[^\s]+|/tmp[^\s]+|/var/folders/[^\s]+", "<tmp>", text)
    text = re.sub(r"\d+\.\d+s\b", "<dur>", text)
    key_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("E ", ">", "assert ")):
            key_lines.append(stripped)
        elif any(token in stripped for token in ("Error", "AssertionError", "FAILED")):
            key_lines.append(stripped)
    if key_lines:
        text = "\n".join(key_lines)
    if len(text) > settings.REPAIR_ERROR_MAX_CHARS:
        text = text[: settings.REPAIR_ERROR_MAX_CHARS]
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# Alias legado.
_error_fingerprint = error_fingerprint
