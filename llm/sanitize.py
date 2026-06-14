from __future__ import annotations

import re

# Padrões de segredo — aplicados somente em texto destinado a persistência/log.
_SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bsk-[a-zA-Z0-9]{10,}\b"), "sk-***"),
    (re.compile(r"\bBearer\s+[a-zA-Z0-9._-]{10,}\b", re.IGNORECASE), "Bearer ***"),
    (
        re.compile(
            r"(?i)([A-Z0-9_]*(?:API[_-]?KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*)\s*[=:]\s*['\"]?[^\s#'\"]{4,}['\"]?"
        ),
        r"\1=***",
    ),
    (re.compile(r"(?i)(password\s*[=:]\s*)['\"]?\S+['\"]?"), r"\1***"),
]


def sanitize_text(text: str) -> str:
    """Remove ou mascara padrões de segredo em texto destinado a logs/arquivos."""
    if not text:
        return text
    result = text
    for pattern, replacement in _SECRET_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def contains_secret_pattern(text: str) -> bool:
    """True se o texto contém um padrão que seria mascarado em logs."""
    if not text:
        return False
    return sanitize_text(text) != text
