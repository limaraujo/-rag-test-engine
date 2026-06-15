from __future__ import annotations

import fnmatch
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from config.security_paths import SENSITIVE_DIR_NAMES, is_sensitive_file_name, is_sensitive_path
from config.settings import ROOT, settings

logger = logging.getLogger(__name__)

DEFAULT_SKIP_DIRS: frozenset[str] = frozenset(
    {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "tests",
        "test",
        "runs",
        "logs",
        "generated_tests",
        "dist",
        "build",
        *SENSITIVE_DIR_NAMES,
    }
)

DEFAULT_SKIP_FILE_GLOBS: tuple[str, ...] = (
    "test_*.py",
    "*_test.py",
    "conftest.py",
    "*_demo.py",
)

def _parse_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def get_skip_dirs() -> frozenset[str]:
    """Defaults + ``INGEST_SKIP_DIRS`` (env), sem remover os padrões."""
    extra = _parse_csv(settings.INGEST_SKIP_DIRS)
    return DEFAULT_SKIP_DIRS | frozenset(extra)


def get_skip_file_globs() -> tuple[str, ...]:
    """Defaults + ``INGEST_SKIP_FILE_GLOBS`` (env), sem remover os padrões."""
    extra = _parse_csv(settings.INGEST_SKIP_FILE_GLOBS)
    seen: set[str] = set()
    merged: list[str] = []
    for pattern in (*DEFAULT_SKIP_FILE_GLOBS, *extra):
        if pattern not in seen:
            seen.add(pattern)
            merged.append(pattern)
    return tuple(merged)


def _part_matches_skip(part: str, skip_dirs: frozenset[str]) -> bool:
    if part in skip_dirs:
        return True
    if sys.platform == "win32":
        lower = part.lower()
        return any(lower == skip_dir.lower() for skip_dir in skip_dirs)
    return False


def _relative_parts(path: Path, root: Path) -> tuple[str, ...]:
    try:
        return path.resolve().relative_to(root.resolve()).parts
    except ValueError:
        return path.parts


def should_skip_python_file(
    path: Path,
    root: Path,
    *,
    skip_dirs: frozenset[str] | None = None,
    skip_globs: tuple[str, ...] | None = None,
) -> bool:
    """True se o arquivo Python deve ser ignorado na ingestão."""
    skip_dirs = skip_dirs if skip_dirs is not None else get_skip_dirs()
    skip_globs = skip_globs if skip_globs is not None else get_skip_file_globs()

    rel_parts = _relative_parts(path, root)
    if not rel_parts:
        return True

    dir_parts = rel_parts[:-1]
    if any(_part_matches_skip(part, skip_dirs) for part in dir_parts):
        return True

    file_name = rel_parts[-1]
    if is_sensitive_file_name(file_name) or is_sensitive_path(path, root):
        return True
    return any(fnmatch.fnmatch(file_name, pattern) for pattern in skip_globs)


@dataclass(frozen=True)
class ScanResult:
    files: tuple[Path, ...]
    total_py_found: int
    excluded: int

    @property
    def included(self) -> int:
        return len(self.files)


def scan_python_files(root: str | Path) -> ScanResult:
    """Descobre arquivos ``.py`` aplicando exclusões centralizadas."""
    root_path = Path(root).resolve()
    skip_dirs = get_skip_dirs()
    skip_globs = get_skip_file_globs()

    included: list[Path] = []
    total = 0
    for path in root_path.rglob("*.py"):
        total += 1
        if should_skip_python_file(
            path,
            root_path,
            skip_dirs=skip_dirs,
            skip_globs=skip_globs,
        ):
            continue
        included.append(path)

    return ScanResult(
        files=tuple(sorted(included)),
        total_py_found=total,
        excluded=total - len(included),
    )


def emit_scan_warnings(root: str | Path, result: ScanResult) -> None:
    """Registra avisos para raiz do engine ou volume anormal de arquivos."""
    root_path = Path(root).resolve()

    if root_path == ROOT.resolve():
        logger.warning(
            "[ingest] diretório analisado é a raiz do RAG test engine (%s); "
            "considere apontar para o código-fonte do projeto alvo",
            root_path,
        )

    warn_threshold = settings.SOURCE_DIR_PY_WARN_THRESHOLD
    if result.included > warn_threshold:
        logger.warning(
            "[ingest] volume alto de arquivos Python incluídos (%d > %d); "
            "verifique se o diretório alvo está correto",
            result.included,
            warn_threshold,
        )

    if result.excluded:
        logger.info(
            "[ingest] exclusões: %d arquivo(s) .py ignorado(s), %d incluído(s)",
            result.excluded,
            result.included,
        )
