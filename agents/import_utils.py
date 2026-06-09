from __future__ import annotations

import re
from pathlib import Path

from ingest.import_resolver import module_name_from_path
from schemas.context import FunctionContext


def import_target(
    context: FunctionContext,
    project_root: Path,
) -> tuple[str, str]:
    """Retorna (módulo Python, nome importado) para o símbolo sob teste."""
    module = context.module_name or module_name_from_path(
        project_root,
        Path(context.file_path),
    )
    if context.class_name:
        return module, context.class_name
    if context.symbol_type == "class":
        return module, context.function_name
    return module, context.function_name


def normalize_test_imports(
    code: str,
    *,
    module: str,
    name: str,
) -> str:
    """Substitui imports incorretos pelo caminho de módulo completo."""
    correct = f"from {module} import {name}"
    lines = code.splitlines()

    filtered = [
        line
        for line in lines
        if not _is_target_import_line(line, name)
    ]

    insert_at = 0
    for index, line in enumerate(filtered):
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")):
            insert_at = index + 1
        elif stripped and not stripped.startswith("#"):
            break

    if not any(line.strip() == correct for line in filtered):
        filtered.insert(insert_at, correct)

    return "\n".join(filtered).strip() + "\n"


def _is_target_import_line(line: str, name: str) -> bool:
    stripped = line.strip()
    if re.match(rf"^import\s+{re.escape(name)}\b", stripped):
        return True
    match = re.match(r"^from\s+(\S+)\s+import\s+(.+)$", stripped)
    if not match:
        return False
    imported = match.group(2)
    return name in {part.strip() for part in imported.split(",")}
