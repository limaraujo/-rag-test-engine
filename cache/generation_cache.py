from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ValidationError

from agents import test_generator as _test_generator_module
from config.settings import ROOT, settings
from retrieval.embedding_builder import content_hash
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest

logger = logging.getLogger(__name__)

EntryStatus = Literal["active", "stale"]


def normalize_source_code(source: str) -> str:
    """Normaliza código-fonte para hashing estável entre plataformas."""
    text = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def source_code_hash(source: str) -> str:
    return content_hash(normalize_source_code(source))


def rag_context_hash(ctx: FunctionContext) -> str:
    """Hash do contexto RAG efetivamente disponível no prompt."""
    parts: list[str] = []
    for item in ctx.related_functions:
        parts.append(content_hash(item))
    for item in ctx.similar_tests:
        parts.append(content_hash(item))

    rc = ctx.retrieval_context
    if rc is not None:
        for item in rc.dependency_functions:
            parts.append(content_hash(item))
        for item in rc.caller_functions:
            parts.append(content_hash(item))
        for item in rc.callee_functions:
            parts.append(content_hash(item))

    if not parts:
        return ""
    return hashlib.sha256("|".join(sorted(parts)).encode()).hexdigest()[:16]


def generation_settings_fingerprint() -> str:
    """Fingerprint de configurações que alteram o prompt ou a geração."""
    values = {
        "generation_max_test_functions": settings.GENERATION_MAX_TEST_FUNCTIONS,
        "generation_max_lines": settings.GENERATION_MAX_LINES,
        "prompt_max_rag_total_chars": settings.PROMPT_MAX_RAG_TOTAL_CHARS,
        "prompt_max_rag_snippet_chars": settings.PROMPT_MAX_RAG_SNIPPET_CHARS,
        "retriever_top_k": settings.RETRIEVER_TOP_K,
        "retriever_top_k_functions": settings.RETRIEVER_TOP_K_FUNCTIONS,
        "retriever_top_k_tests": settings.RETRIEVER_TOP_K_TESTS,
        "retriever_rerank_pool_size": settings.RETRIEVER_RERANK_POOL_SIZE,
        "retriever_vector_weight": settings.RETRIEVER_VECTOR_WEIGHT,
        "retriever_dependency_weight": settings.RETRIEVER_DEPENDENCY_WEIGHT,
        "retriever_call_graph_weight": settings.RETRIEVER_CALL_GRAPH_WEIGHT,
        "retriever_score_threshold": settings.RETRIEVER_SCORE_THRESHOLD,
    }
    payload = json.dumps(values, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


class CachedGenerationEntry(BaseModel):
    """Entrada persistida no cache de geração (sem prompts nem segredos)."""

    schema_version: int
    cache_key: str
    qualified_name: str
    source_hash: str
    model: str
    prompt_version: str
    generator_version: str
    settings_fingerprint: str
    operation: str
    rag_context_hash: str | None = None
    status: EntryStatus = "active"
    stale_reason: str | None = None
    stale_at: str | None = None
    created_at: str
    generated_test: dict[str, Any]
    coverage: dict[str, Any] | None = None


class GenerationCache:
    """Cache persistente de testes gerados e aprovados."""

    def __init__(self, cache_dir: Path | None = None) -> None:
        self._cache_dir = cache_dir

    @property
    def enabled(self) -> bool:
        return settings.GENERATION_CACHE_ENABLED

    @property
    def cache_dir(self) -> Path:
        if self._cache_dir is not None:
            return self._cache_dir
        configured = settings.GENERATION_CACHE_DIR
        if configured:
            path = Path(configured)
            if not path.is_absolute():
                path = ROOT / path
            return path
        return ROOT / ".cache" / "generation"

    def build_cache_key(
        self,
        ctx: FunctionContext,
        *,
        operation: str,
        model: str,
        rag_hash: str | None = None,
    ) -> str:
        rag_part = rag_hash or rag_context_hash(ctx) or "no-rag"
        parts = [
            ctx.qualified_name,
            source_code_hash(ctx.code),
            model,
            _test_generator_module.PROMPT_VERSION,
            generation_settings_fingerprint(),
            _test_generator_module.GENERATOR_VERSION,
            operation,
            rag_part,
        ]
        digest = hashlib.sha256("|".join(parts).encode()).hexdigest()
        return digest

    def _entry_path(self, cache_key: str) -> Path:
        safe = re.sub(r"[^a-f0-9]", "", cache_key.lower())
        shard = safe[:2] or "00"
        return self.cache_dir / shard / f"{safe}.json"

    def lookup(
        self,
        ctx: FunctionContext,
        *,
        operation: str,
        model: str,
    ) -> CachedGenerationEntry | None:
        if not self.enabled:
            return None

        cache_key = self.build_cache_key(ctx, operation=operation, model=model)
        path = self._entry_path(cache_key)
        if not path.is_file():
            return None

        raw = self._read_json(path)
        if raw is None:
            return None

        entry = self._validate_entry(raw, expected_key=cache_key)
        if entry is None:
            return None
        if entry.status == "stale":
            return None
        return entry

    def materialize(self, entry: CachedGenerationEntry) -> GeneratedTest:
        return GeneratedTest.model_validate(entry.generated_test)

    def mark_stale(self, cache_key: str, *, reason: str) -> None:
        if not self.enabled:
            return

        path = self._entry_path(cache_key)
        raw = self._read_json(path)
        if raw is None:
            return

        entry = self._validate_entry(raw, expected_key=cache_key)
        if entry is None:
            return

        updated = entry.model_copy(
            update={
                "status": "stale",
                "stale_reason": reason,
                "stale_at": _utc_now(),
            }
        )
        self._write_entry(path, updated)

    def save(
        self,
        ctx: FunctionContext,
        test: GeneratedTest,
        *,
        operation: str,
        model: str,
        coverage: dict[str, Any] | None = None,
    ) -> Path | None:
        if not self.enabled:
            return None

        cache_key = self.build_cache_key(ctx, operation=operation, model=model)
        entry = CachedGenerationEntry(
            schema_version=settings.GENERATION_CACHE_SCHEMA_VERSION,
            cache_key=cache_key,
            qualified_name=ctx.qualified_name,
            source_hash=source_code_hash(ctx.code),
            model=model,
            prompt_version=_test_generator_module.PROMPT_VERSION,
            generator_version=_test_generator_module.GENERATOR_VERSION,
            settings_fingerprint=generation_settings_fingerprint(),
            operation=operation,
            rag_context_hash=rag_context_hash(ctx) or None,
            status="active",
            created_at=_utc_now(),
            generated_test=test.model_dump(),
            coverage=coverage,
        )
        path = self._entry_path(cache_key)
        self._write_entry(path, entry)
        return path

    def _validate_entry(
        self,
        raw: dict[str, Any],
        *,
        expected_key: str,
    ) -> CachedGenerationEntry | None:
        try:
            if raw.get("schema_version") != settings.GENERATION_CACHE_SCHEMA_VERSION:
                logger.warning(
                    "generation cache schema mismatch for %s (got %r, want %d)",
                    expected_key[:12],
                    raw.get("schema_version"),
                    settings.GENERATION_CACHE_SCHEMA_VERSION,
                )
                return None

            entry = CachedGenerationEntry.model_validate(raw)
            if entry.cache_key != expected_key:
                logger.warning(
                    "generation cache key mismatch for %s",
                    expected_key[:12],
                )
                return None
            return entry
        except ValidationError as exc:
            logger.warning(
                "generation cache entry invalid for %s: %s",
                expected_key[:12],
                exc.errors()[0]["msg"] if exc.errors() else exc,
            )
            return None

    def _read_json(self, path: Path) -> dict[str, Any] | None:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("generation cache read failed for %s: %s", path, exc)
            return None

    def _write_entry(self, path: Path, entry: CachedGenerationEntry) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            entry.model_dump(),
            indent=2,
            ensure_ascii=False,
        )
        self._atomic_write(path, payload)

    @staticmethod
    def _atomic_write(path: Path, payload: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{path.stem}.",
            suffix=".tmp",
            dir=path.parent,
        )
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
