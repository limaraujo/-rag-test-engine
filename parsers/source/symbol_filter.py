from __future__ import annotations

import ast
import fnmatch
from dataclasses import dataclass
from pathlib import Path

from config.settings import settings
from parsers.source.models.ExtractedSymbol import ExtractedSymbol
from parsers.source.path_filters import get_skip_file_globs


@dataclass(frozen=True)
class SymbolFilterStats:
    extracted_total: int = 0
    filtered_total: int = 0
    removed_container_class: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "extracted_total": self.extracted_total,
            "filtered_total": self.filtered_total,
            "removed_container_class": self.removed_container_class,
        }


@dataclass(frozen=True)
class SymbolFilterResult:
    kept: list[ExtractedSymbol]
    stats: SymbolFilterStats


def _csv_set(value: str) -> set[str]:
    return {part.strip() for part in value.split(",") if part.strip()}


def _classes_with_extracted_methods(
    symbols: list[ExtractedSymbol],
) -> set[tuple[str, str]]:
    """``(file_path, class_name)`` para classes que possuem métodos extraídos."""
    keys: set[tuple[str, str]] = set()
    for symbol in symbols:
        if symbol.symbol_type == "method" and symbol.class_name:
            keys.add((symbol.file_path, symbol.class_name))
    return keys


def _parse_class_def(source_code: str) -> ast.ClassDef | None:
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return None

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            return node
    return None


def _class_body_has_executable_behavior(class_def: ast.ClassDef) -> bool:
    """True quando o corpo da classe tem statements executáveis fora de funções aninhadas."""
    for stmt in class_def.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(stmt, ast.Pass):
            continue
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            continue
        if isinstance(stmt, ast.AnnAssign) and stmt.value is None:
            continue
        return True
    return False


def _class_has_own_executable_behavior(symbol: ExtractedSymbol) -> bool:
    class_def = _parse_class_def(symbol.source_code)
    if class_def is None:
        return False
    return _class_body_has_executable_behavior(class_def)


def should_generate_tests(
    symbol: ExtractedSymbol,
    *,
    classes_with_methods: set[tuple[str, str]] | None = None,
) -> bool:
    """Retorna False para símbolos que não devem gerar testes."""
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

    if symbol.symbol_type == "class":
        if classes_with_methods and (symbol.file_path, symbol.name) in classes_with_methods:
            return False
        if not _class_has_own_executable_behavior(symbol):
            return False

    return True


def filter_symbols(symbols: list[ExtractedSymbol]) -> SymbolFilterResult:
    """Filtra símbolos elegíveis para geração de testes e agrega estatísticas."""
    extracted_total = len(symbols)
    classes_with_methods = _classes_with_extracted_methods(symbols)

    kept: list[ExtractedSymbol] = []
    removed_container_class = 0

    for symbol in symbols:
        if not should_generate_tests(
            symbol,
            classes_with_methods=classes_with_methods,
        ):
            if (
                symbol.symbol_type == "class"
                and (symbol.file_path, symbol.name) in classes_with_methods
            ):
                removed_container_class += 1
            continue
        kept.append(symbol)

    filtered_total = extracted_total - len(kept)
    return SymbolFilterResult(
        kept=kept,
        stats=SymbolFilterStats(
            extracted_total=extracted_total,
            filtered_total=filtered_total,
            removed_container_class=removed_container_class,
        ),
    )


def filter_symbols_for_tests(symbols: list[ExtractedSymbol]) -> list[ExtractedSymbol]:
    return filter_symbols(symbols).kept
