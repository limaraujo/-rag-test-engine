from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path

logger = logging.getLogger(__name__)

_TRUNCATED_SUFFIX = "\n… (truncado)"
_HEADERS_PATH = Path(__file__).resolve().parent / "rag_headers.yaml"


def _load_rag_section_headers() -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in _HEADERS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        headers[key.strip()] = value.strip().strip('"').strip("'")
    return headers


# Cabeçalhos de seção RAG não entram em PROMPT_MAX_RAG_TOTAL_CHARS (corpo dos snippets).
RAG_SECTION_HEADERS: dict[str, str] = _load_rag_section_headers()


class RagCategory(IntEnum):
    """Prioridade crescente — valor menor = maior prioridade no prompt."""

    DEPENDENCY = 0
    CALLEE = 1
    CALLER = 2
    RELATED = 3
    SIMILAR_TEST = 4


@dataclass
class RagItem:
    content: str
    category: RagCategory
    stable_id: str | None = None
    qualified_name: str | None = None


@dataclass
class RagPromptMetrics:
    candidates_total: int = 0
    candidates_by_category: dict[str, int] = field(default_factory=dict)
    after_dedup: int = 0
    chars_before: int = 0
    chars_after: int = 0
    dropped_by_budget: list[str] = field(default_factory=list)
    estimated_tokens: int | None = None

    def log_summary(self) -> str:
        cats = " ".join(f"{k}={v}" for k, v in sorted(self.candidates_by_category.items()))
        dropped = len(self.dropped_by_budget)
        tok = (
            f" estimated_tokens={self.estimated_tokens}"
            if self.estimated_tokens is not None
            else ""
        )
        return (
            f"rag_prompt candidates={self.candidates_total} ({cats}) "
            f"dedup={self.after_dedup} "
            f"chars={self.chars_before}->{self.chars_after} "
            f"dropped_budget={dropped}{tok}"
        )


def truncate_utf8(text: str, max_chars: int, *, suffix: str = _TRUNCATED_SUFFIX) -> str:
    """
    Trunca em limite de code points Unicode (nunca parte um caractere UTF-8).
    """
    if max_chars <= 0:
        return ""
    if len(text) <= max_chars:
        return text
    if len(suffix) >= max_chars:
        return truncate_utf8(suffix, max_chars, suffix="")
    body_budget = max_chars - len(suffix)
    return text[:body_budget] + suffix


def compact_rag_snippet(text: str, *, max_chars: int, label: str = "") -> str:
    """
    Reduz trechos RAG para o prompt: extrai só o código quando possível e trunca.
    """
    stripped = text.strip()
    if "code:\n" in stripped:
        stripped = stripped.split("code:\n", 1)[1].strip()
    elif stripped.startswith("symbol:"):
        lines = stripped.split("\n", 1)
        stripped = lines[1].strip() if len(lines) > 1 else stripped

    if label and not stripped.startswith(label):
        stripped = f"{label}\n{stripped}"

    return truncate_utf8(stripped, max_chars)


def _normalize_content(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _code_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _extract_code_body(content: str) -> str:
    stripped = content.strip()
    if "code:\n" in stripped:
        return stripped.split("code:\n", 1)[1].strip()
    if stripped.startswith("symbol:"):
        parts = stripped.split("\n", 1)
        return parts[1].strip() if len(parts) > 1 else stripped
    return stripped


def _parse_qualified_name(content: str) -> str | None:
    stripped = content.strip()
    if stripped.startswith("symbol:"):
        first = stripped.split("\n", 1)[0]
        return first.split(":", 1)[1].strip() or None
    return None


def identity_key(item: RagItem) -> str:
    if item.stable_id:
        return f"id:{item.stable_id}"
    qname = item.qualified_name or _parse_qualified_name(item.content)
    if qname:
        return f"qn:{qname}"
    code = _extract_code_body(item.content)
    if code:
        return f"hash:{_code_hash(code)}"
    return f"norm:{_code_hash(_normalize_content(item.content))}"


def deduplicate_rag_items(items: list[RagItem]) -> list[RagItem]:
    """Mantém a ocorrência de maior prioridade por identidade estável."""
    kept: dict[str, RagItem] = {}
    for category in RagCategory:
        for item in items:
            if item.category != category:
                continue
            key = identity_key(item)
            if key not in kept:
                kept[key] = item

    order = {cat: idx for idx, cat in enumerate(RagCategory)}
    return sorted(
        kept.values(),
        key=lambda item: (order[item.category], identity_key(item)),
    )


def _format_bullet(items: list[str]) -> str:
    if not items:
        return "  (nenhum)"
    return "\n".join(f"  - {item}" for item in items)


def _snippet_body_chars(items: list[str]) -> int:
    if not items:
        return 0
    bullets = _format_bullet(items)
    return len(bullets)


def build_rag_prompt_sections(
    items: list[RagItem],
    *,
    max_total_chars: int,
    max_snippet_chars: int,
    log_metrics: bool = True,
) -> tuple[list[str], RagPromptMetrics]:
    """
    Deduplica, trunca e aplica orçamento global ao bloco RAG do prompt.

    O orçamento ``max_total_chars`` aplica-se apenas ao corpo dos snippets
    (texto das bullets). Cabeçalhos de seção (``RAG_SECTION_HEADERS``) ficam
    fora desse limite.
    """
    metrics = RagPromptMetrics()
    if not items:
        if log_metrics:
            logger.info(metrics.log_summary())
        return [], metrics

    metrics.candidates_total = len(items)
    for cat in RagCategory:
        count = sum(1 for item in items if item.category == cat)
        if count:
            metrics.candidates_by_category[cat.name.lower()] = count

    deduped = deduplicate_rag_items(items)
    metrics.after_dedup = len(deduped)

    truncated: list[RagItem] = []
    for item in deduped:
        snippet = compact_rag_snippet(item.content, max_chars=max_snippet_chars)
        truncated.append(
            RagItem(
                content=snippet,
                category=item.category,
                stable_id=item.stable_id,
                qualified_name=item.qualified_name or _parse_qualified_name(item.content),
            )
        )

    by_category: dict[RagCategory, list[RagItem]] = {cat: [] for cat in RagCategory}
    for item in truncated:
        by_category[item.category].append(item)

    bodies: dict[RagCategory, list[str]] = {
        cat: [item.content for item in group] for cat, group in by_category.items()
    }
    metrics.chars_before = sum(_snippet_body_chars(body) for body in bodies.values())

    total_body = metrics.chars_before
    if total_body > max_total_chars:
        for category in reversed(list(RagCategory)):
            group = by_category[category]
            while group and total_body > max_total_chars:
                removed = group.pop()
                label = removed.qualified_name or identity_key(removed)
                metrics.dropped_by_budget.append(f"{category.name}:{label}")
                bodies[category] = [item.content for item in group]
                total_body = sum(_snippet_body_chars(body) for body in bodies.values())

    metrics.chars_after = sum(_snippet_body_chars(body) for body in bodies.values())
    if metrics.chars_after:
        metrics.estimated_tokens = max(1, metrics.chars_after // 4)

    sections: list[str] = []
    for category in RagCategory:
        body_items = bodies[category]
        if not body_items:
            continue
        header_key = category.name.lower()
        header = RAG_SECTION_HEADERS[header_key]
        sections.append(f"\n{header}\n{_format_bullet(body_items)}")

    if log_metrics:
        logger.info(metrics.log_summary())

    return sections, metrics


def rag_items_from_lists(
    *,
    dependency_functions: list[str] | None = None,
    callee_functions: list[str] | None = None,
    caller_functions: list[str] | None = None,
    related_functions: list[str] | None = None,
    similar_tests: list[str] | None = None,
) -> list[RagItem]:
    """Monta itens RAG a partir das listas do retriever."""

    def _items(values: list[str] | None, category: RagCategory) -> list[RagItem]:
        return [
            RagItem(content=text, category=category, qualified_name=_parse_qualified_name(text))
            for text in (values or [])
            if text and text.strip()
        ]

    return [
        *_items(dependency_functions, RagCategory.DEPENDENCY),
        *_items(callee_functions, RagCategory.CALLEE),
        *_items(caller_functions, RagCategory.CALLER),
        *_items(related_functions, RagCategory.RELATED),
        *_items(similar_tests, RagCategory.SIMILAR_TEST),
    ]
