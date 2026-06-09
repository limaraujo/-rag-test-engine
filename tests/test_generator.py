"""
Testa as funções auxiliares de parsing da saída do LLM.

ESCOPO: apenas lógica pura de string — sem LLM, sem mock, sem API.

As funções _strip_markdown, _extract_imports e _extract_coverage_hints
são utilitários que processam o texto retornado pelo LLM. Elas têm valor
de teste independente porque são chamadas tanto pelo TestGeneratorAgent
quanto pelo RepairAgent, e um bug nelas afeta toda a geração de testes.

O que NÃO está aqui (e por quê):
  - Testes de TestGeneratorAgent.generate() com LLM mockado foram removidos.
    Testar um MagicMock não valida comportamento real; esses testes só fazem
    sentido em testes de integração com a API real ou quando a interface do
    LLM mudar de forma significativa.
"""
from __future__ import annotations

from textwrap import dedent

from agents.test_generator import (
    _extract_coverage_hints,
    _extract_imports,
    _strip_markdown,
)


# ── _strip_markdown ───────────────────────────────────────────────────────────

def test_strip_markdown_removes_python_fence() -> None:
    raw = "```python\nimport pytest\n```"
    assert _strip_markdown(raw) == "import pytest"


def test_strip_markdown_removes_plain_fence() -> None:
    raw = "```\nimport pytest\n```"
    assert _strip_markdown(raw) == "import pytest"


def test_strip_markdown_passthrough_when_no_fence() -> None:
    code = "import pytest\ndef test_foo(): pass"
    assert _strip_markdown(code) == code


def test_strip_markdown_multiline_code_block() -> None:
    raw = dedent("""\
        ```python
        import pytest

        def test_add():
            assert 1 + 1 == 2
        ```
    """).strip()
    result = _strip_markdown(raw)
    assert "import pytest" in result
    assert "def test_add" in result
    assert "```" not in result


def test_strip_markdown_strips_surrounding_whitespace() -> None:
    raw = "\n\n```python\nimport os\n```\n\n"
    assert _strip_markdown(raw) == "import os"


# ── _extract_imports ──────────────────────────────────────────────────────────

def test_extract_imports_finds_import_lines() -> None:
    code = dedent("""\
        import pytest
        from pathlib import Path
        from calc import divide

        def test_foo():
            pass
    """)
    imports = _extract_imports(code)
    assert "import pytest" in imports
    assert "from pathlib import Path" in imports
    assert "from calc import divide" in imports


def test_extract_imports_excludes_non_import_lines() -> None:
    code = "import pytest\ndef test_foo():\n    x = 'from somewhere'\n"
    imports = _extract_imports(code)
    assert imports == ["import pytest"]


def test_extract_imports_empty_code() -> None:
    assert _extract_imports("") == []


# ── _extract_coverage_hints ───────────────────────────────────────────────────

def test_extract_coverage_hints_uses_docstring() -> None:
    code = dedent("""\
        def test_divide_normal():
            \"\"\"Divides two positive integers and returns float.\"\"\"
            assert divide(10, 2) == 5.0
    """)
    hints = _extract_coverage_hints(code)
    assert len(hints) == 1
    assert "test_divide_normal" in hints[0]
    assert "Divides two positive" in hints[0]


def test_extract_coverage_hints_falls_back_to_name_only() -> None:
    code = dedent("""\
        def test_divide_by_zero():
            with pytest.raises(ValueError):
                divide(1, 0)
    """)
    hints = _extract_coverage_hints(code)
    assert hints == ["test_divide_by_zero"]


def test_extract_coverage_hints_multiple_tests() -> None:
    code = dedent("""\
        def test_add_positive():
            \"\"\"Happy path.\"\"\"
            assert add(1, 2) == 3

        def test_add_negative():
            \"\"\"Negative integers.\"\"\"
            assert add(-1, -2) == -3
    """)
    hints = _extract_coverage_hints(code)
    assert len(hints) == 2


def test_extract_coverage_hints_empty_code() -> None:
    assert _extract_coverage_hints("") == []