"""Parsing de respostas LLM (código de teste gerado ou reparado)."""

from __future__ import annotations

import ast
import logging
import re

from agents.import_utils import import_target, normalize_test_imports
from config.settings import ROOT, settings
from parsers.source.text_utils import strip_utf8_bom
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest

logger = logging.getLogger(__name__)


class EmptyGenerationError(ValueError):
    """Resposta do LLM sem código de teste."""


class TruncatedGenerationError(ValueError):
    """Resposta do LLM aparentemente truncada antes de completar o código."""


def parse_response(raw: str, context: FunctionContext) -> GeneratedTest:
    code = normalize_code_response(raw)
    validate_syntax(code)
    warn_generation_limits(code)
    module, name = import_target(context, ROOT)
    code = normalize_test_imports(code, module=module, name=name)
    return GeneratedTest(
        target_function=context.qualified_name,
        imports=extract_imports(code),
        code=code,
        coverage_hints=extract_coverage_hints(code),
    )


def normalize_code_response(raw: str) -> str:
    text = strip_utf8_bom(raw.strip())
    if not text:
        raise EmptyGenerationError("LLM returned empty test code")

    if has_markdown_fence(text):
        text = strip_markdown(text)
        if not text:
            raise EmptyGenerationError("LLM returned empty test code after removing markdown fences")

    raise_if_truncated(text, raw)
    return text


def has_markdown_fence(text: str) -> bool:
    return text.startswith("```") or "```python" in text or re.search(r"^```\w*\s*$", text, re.MULTILINE)


def strip_markdown(text: str) -> str:
    """
    Remove cercas markdown quando o LLM envolve a saída nelas.

    Lida com ```python\\n...\\n``` e ```\\n...\\n```.
    """
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()

    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return text


def raise_if_truncated(code: str, raw: str) -> None:
    if raw.count("```") % 2 == 1:
        raise TruncatedGenerationError("LLM response has unclosed markdown fence")

    stripped = code.rstrip()
    if not stripped:
        raise EmptyGenerationError("LLM returned empty test code")

    last_line = stripped.splitlines()[-1].strip()
    if last_line.endswith(("\\", "(", "[", "{", ",", ":")):
        raise TruncatedGenerationError(f"LLM response ends with incomplete line: {last_line!r}")

    if re.search(r"\bdef test_\w*$", last_line):
        raise TruncatedGenerationError("LLM response ends with incomplete test function definition")


def validate_syntax(code: str) -> None:
    ast.parse(code)


def count_test_functions(code: str) -> int:
    return sum(
        1 for line in code.splitlines()
        if line.strip().startswith("def test_")
    )


def warn_generation_limits(code: str) -> None:
    num_tests = count_test_functions(code)
    num_lines = len(code.splitlines())
    max_fn = settings.GENERATION_MAX_TEST_FUNCTIONS
    max_lines = settings.GENERATION_MAX_LINES

    if num_tests > max_fn:
        logger.warning(
            "generated test has %d test functions (limit %d)",
            num_tests,
            max_fn,
        )
    if num_lines > max_lines:
        logger.warning(
            "generated test has %d lines (limit %d)",
            num_lines,
            max_lines,
        )


def extract_imports(code: str) -> list[str]:
    """Retorna todas as linhas de import de nível superior do código gerado."""
    return [
        line.strip()
        for line in code.splitlines()
        if re.match(r"^(import |from )\S", line.strip())
    ]


def _extract_coverage_hint_text(lines: list[str], test_line_index: int) -> str:
    """Extrai docstring ou comentário # imediatamente acima/abaixo da função de teste."""
    for j in range(test_line_index + 1, min(test_line_index + 5, len(lines))):
        inner = lines[j].strip()
        if inner.startswith('"""') or inner.startswith("'''"):
            return inner.strip('"""').strip("'''").strip()
        if inner:
            break

    comment_lines: list[str] = []
    for j in range(test_line_index - 1, max(-1, test_line_index - 6), -1):
        prev = lines[j].strip()
        if prev.startswith("#"):
            comment_lines.insert(0, prev.lstrip("#").strip())
            continue
        if prev.startswith("@pytest.mark.parametrize"):
            continue
        if not prev:
            continue
        break

    return " ".join(comment_lines)


def extract_coverage_hints(code: str) -> list[str]:
    """
    Constrói dicas de cobertura a partir dos nomes das funções de teste.

    Inclui comentário # ou docstring de uma linha quando presente; caso contrário usa só o nome.
    """
    hints: list[str] = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("def test_"):
            continue

        name = stripped.split("(")[0].removeprefix("def ")

        parametrize_hint = ""
        for j in range(max(0, i - 3), i):
            prev = lines[j].strip()
            if prev.startswith("@pytest.mark.parametrize"):
                parametrize_hint = " (parametrize)"
                break

        hint_text = _extract_coverage_hint_text(lines, i)

        label = f"{name}{parametrize_hint}"
        hints.append(f"{label}: {hint_text}" if hint_text else label)

    return hints
