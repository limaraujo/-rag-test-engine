from __future__ import annotations

import re

# Padrões básicos de segredo — aplicados antes de qualquer log textual.
_SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bsk-[a-zA-Z0-9]{10,}\b"), "sk-***"),
    (re.compile(r"\bBearer\s+[a-zA-Z0-9._-]{10,}\b", re.IGNORECASE), "Bearer ***"),
    (re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)['\"]?[a-zA-Z0-9._-]{8,}['\"]?"), r"\1***"),
    (re.compile(r"(?i)(OPENAI_API_KEY\s*=\s*)\S+"), r"\1***"),
    (re.compile(r"(?i)(QDRANT_API_KEY\s*=\s*)\S+"), r"\1***"),
    (re.compile(r"(?i)(password\s*[=:]\s*)['\"]?\S+['\"]?"), r"\1***"),
]


def sanitize_text(text: str) -> str:
    """Remove ou mascara padrões de segredo em texto destinado a logs."""
    if not text:
        return text
    result = text
    for pattern, replacement in _SECRET_PATTERNS:
        result = pattern.sub(replacement, result)
    return result
