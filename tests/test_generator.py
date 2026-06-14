"""
Testa prompt, parsing e validação da saída do LLM na geração de testes.

ESCOPO: lógica pura — sem LLM real, sem mock de API.
"""
from __future__ import annotations

import logging
from textwrap import dedent

import pytest

from agents.test_generator import (
    EmptyGenerationError,
    TruncatedGenerationError,
    _build_system_prompt,
    _extract_coverage_hints,
    _extract_imports,
    _normalize_code_response,
    _parse_response,
    _strip_markdown,
    _validate_syntax,
    _warn_generation_limits,
)
from config.settings import settings
from schemas.context import FunctionContext


def _ctx() -> FunctionContext:
    return FunctionContext(
        function_name="divide",
        qualified_name="divide",
        symbol_type="function",
        file_path="calc.py",
        module_name="calc",
        code="def divide(a, b):\n    return a / b",
    )


def _valid_code() -> str:
    return dedent("""\
        import pytest
        from calc import divide

        def test_divide_happy():
            assert divide(10, 2) == 5.0
    """).strip()


# ── Prompt ────────────────────────────────────────────────────────────────────

def test_prompt_does_not_require_docstrings() -> None:
    prompt = _build_system_prompt()
    assert "docstring" in prompt.lower()
    assert "sem docstrings" in prompt.lower() or "sem docstring" in prompt.lower()
    assert "uma docstring" not in prompt.lower()
    assert "adicione uma docstring" not in prompt.lower()


def test_prompt_includes_limits() -> None:
    prompt = _build_system_prompt()
    assert str(settings.GENERATION_MAX_TEST_FUNCTIONS) in prompt
    assert str(settings.GENERATION_MAX_LINES) in prompt
    assert "funções test_" in prompt.lower() or "funções test_*" in prompt.lower()


def test_prompt_requests_concise_output() -> None:
    prompt = _build_system_prompt()
    assert "concis" in prompt.lower()
    assert "menor conjunto" in prompt.lower()


def test_prompt_requests_parametrize() -> None:
    prompt = _build_system_prompt()
    assert "parametrize" in prompt.lower()


# ── _strip_markdown / _normalize_code_response ────────────────────────────────

def test_strip_markdown_removes_python_fence() -> None:
    raw = "```python\nimport pytest\n```"
    assert _strip_markdown(raw) == "import pytest"


def test_strip_markdown_removes_plain_fence() -> None:
    raw = "```\nimport pytest\n```"
    assert _strip_markdown(raw) == "import pytest"


def test_strip_markdown_passthrough_when_no_fence() -> None:
    code = "import pytest\ndef test_foo(): pass"
    assert _normalize_code_response(code) == code


def test_strip_markdown_multiline_code_block() -> None:
    raw = dedent("""\
        ```python
        import pytest

        def test_add():
            assert 1 + 1 == 2
        ```
    """).strip()
    result = _normalize_code_response(raw)
    assert "import pytest" in result
    assert "def test_add" in result
    assert "```" not in result


def test_strip_markdown_strips_surrounding_whitespace() -> None:
    raw = "\n\n```python\nimport os\n```\n\n"
    assert _normalize_code_response(raw) == "import os"


def test_fence_response_normalized_via_parse() -> None:
    raw = f"```python\n{_valid_code()}\n```"
    parsed = _parse_response(raw, _ctx())
    assert "def test_divide_happy" in parsed.code
    assert "```" not in parsed.code


def test_empty_response_fails_explicitly() -> None:
    with pytest.raises(EmptyGenerationError, match="empty"):
        _normalize_code_response("")
    with pytest.raises(EmptyGenerationError, match="empty"):
        _normalize_code_response("   \n  ")


def test_truncated_response_fails_explicitly() -> None:
    raw = "```python\nimport pytest\n\ndef test_foo("
    with pytest.raises(TruncatedGenerationError):
        _normalize_code_response(raw)


def test_invalid_syntax_is_detected() -> None:
    with pytest.raises(SyntaxError):
        _validate_syntax("def test_x(:\n    pass")


def test_output_over_limit_generates_warning(caplog: pytest.LogCaptureFixture) -> None:
    lines = ["import pytest", "from calc import divide", ""]
    for i in range(settings.GENERATION_MAX_TEST_FUNCTIONS + 2):
        lines.append(f"def test_case_{i}():")
        lines.append("    assert True")
        lines.append("")
    code = "\n".join(lines)

    with caplog.at_level(logging.WARNING, logger="agents.test_generator"):
        _warn_generation_limits(code)

    assert any("test functions" in r.message for r in caplog.records)


def test_lines_over_limit_generates_warning(caplog: pytest.LogCaptureFixture) -> None:
    code = "\n".join(f"x_{i} = {i}" for i in range(settings.GENERATION_MAX_LINES + 5))

    with caplog.at_level(logging.WARNING, logger="agents.test_generator"):
        _warn_generation_limits(code)

    assert any("lines" in r.message for r in caplog.records)


def test_parametrize_test_accepted() -> None:
    code = dedent("""\
        import pytest
        from calc import divide

        @pytest.mark.parametrize("a,b,expected", [(10, 2, 5.0)])
        def test_divide(a, b, expected):
            assert divide(a, b) == expected
    """).strip()
    parsed = _parse_response(code, _ctx())
    assert parsed.test_function_names() == ["test_divide"]
    hints = _extract_coverage_hints(parsed.code)
    assert len(hints) == 1
    assert "parametrize" in hints[0]


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

def test_extract_coverage_hints_uses_docstring_when_present() -> None:
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
            assert add(1, 2) == 3

        def test_add_negative():
            assert add(-1, -2) == -3
    """)
    hints = _extract_coverage_hints(code)
    assert len(hints) == 2


def test_extract_coverage_hints_empty_code() -> None:
    assert _extract_coverage_hints("") == []
