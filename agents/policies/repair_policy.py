"""Heurísticas para decidir se o loop de reparo deve rodar."""

from __future__ import annotations

import re
from pathlib import Path

from execution.runner import RunResult
from schemas.context import FunctionContext

_IMPORT_ERRORS = re.compile(r"(ModuleNotFoundError|ImportError)")
_PYTEST_ERROR_LINE = re.compile(r"^\s*E\s+(ModuleNotFoundError|ImportError)")


def _source_trace_line_pattern(source_name: str) -> re.Pattern[str]:
    """``calc.py:12:`` sem casar ``test_calc.py:12:``."""
    escaped = re.escape(source_name)
    return re.compile(rf"(?:^|[/\\]){escaped}:\d+:")


def skip_repair_reason(result: RunResult, ctx: FunctionContext) -> str | None:
    """
    Retorna um ``stop_reason`` quando o reparo provavelmente não ajuda.

    Erros estruturais/ambientais (coleta pytest, dependência ausente no código-fonte)
    não são corrigíveis reescrevendo o arquivo de teste.
    """
    if result.passed:
        return None

    if result.exit_code == 2:
        return "repair_skipped:pytest_collection_error"

    text = (result.failure_summary or result.output).strip()

    if text and _import_error_in_source_module(text, ctx):
        return "repair_skipped:source_import_dependency"

    collected = result.num_passed + result.num_failed
    if result.num_errors > 0 and collected == 0:
        return "repair_skipped:pytest_setup_error"

    if not text:
        return None

    return None


def _import_error_in_source_module(text: str, ctx: FunctionContext) -> bool:
    """
    Detecta falha de import ao carregar o módulo sob teste (não o arquivo de teste).

    Ex.: o teste importa ``pkg.foo`` corretamente, mas ``foo.py`` faz ``import django``.
    """
    source_name = Path(ctx.file_path).name
    if source_name not in text or not _IMPORT_ERRORS.search(text):
        return False

    source_line = _source_trace_line_pattern(source_name)
    lines = text.splitlines()
    source_seen = False
    for line in lines:
        if source_line.search(line):
            source_seen = True
            continue
        if source_seen and _PYTEST_ERROR_LINE.match(line):
            return True
        if source_seen and _IMPORT_ERRORS.search(line) and line.strip().startswith("E "):
            return True
    return False
