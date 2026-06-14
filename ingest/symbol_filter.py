from __future__ import annotations

import fnmatch
from pathlib import Path

from config.settings import settings
from ingest.models.ExtractedSymbol import ExtractedSymbol
from ingest.path_filters import get_skip_file_globs


def _csv_set(value: str) -> set[str]:
    return {part.strip() for part in value.split(",") if part.strip()}


def should_generate_tests(symbol: ExtractedSymbol) -> bool:
    """Retorna False para símbolos que não devem gerar testes (ex.: ``main`` em scripts)."""
    skip_names = _csv_set(settings.INGEST_SKIP_FUNCTION_NAMES)
    skip_globs = get_skip_file_globs()

    file_name = Path(symbol.file_path).name
    if any(fnmatch.fnmatch(file_name, pattern) for pattern in skip_globs):
        return False

    if (
        symbol.symbol_type == "function"
        and symbol.class_name is None
        and symbol.name in skip_names
    ):
        return False

    return True


def filter_symbols_for_tests(symbols: list[ExtractedSymbol]) -> list[ExtractedSymbol]:
    return [symbol for symbol in symbols if should_generate_tests(symbol)]
