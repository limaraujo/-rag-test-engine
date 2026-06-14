"""
Tests for agents/repair.py prompt construction (_build_repair_prompt).

Scope: prompt assembly only — no LLM, no API mocks.
"""
from __future__ import annotations

import pytest

from agents.repair import _build_repair_prompt
from execution.runner import RunResult
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from tests.conftest import make_symbol


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _ctx() -> FunctionContext:
    return FunctionContext.from_symbol(
        make_symbol("divide", "def divide(a, b):\n    return a / b")
    )


def _failing_test() -> GeneratedTest:
    return GeneratedTest(
        target_function="divide",
        imports=["import pytest", "from wrong_module import divide"],
        code="import pytest\nfrom wrong_module import divide\n\ndef test_divide():\n    assert divide(10, 2) == 0",
        coverage_hints=[],
    )


def _failed_result(stdout: str = "ModuleNotFoundError: No module named 'wrong_module'") -> RunResult:
    return RunResult(
        passed=False,
        exit_code=1,
        stdout=stdout,
        stderr="",
        duration_seconds=0.05,
        test_file="/tmp/test_divide.py",
        num_failed=1,
    )


# ── _build_repair_prompt (Portuguese section headers match repair.py) ───────

def test_build_repair_prompt_has_attempt_header() -> None:
    prompt = _build_repair_prompt(_ctx(), _failing_test(), _failed_result(), attempt=2)
    assert "tentativa de reparo 2" in prompt.lower()


def test_build_repair_prompt_has_all_sections() -> None:
    prompt = _build_repair_prompt(_ctx(), _failing_test(), _failed_result(), attempt=1)
    assert "Função sob teste" in prompt
    assert "Arquivo de teste falho" in prompt
    assert "Saída de erro do pytest" in prompt


def test_build_repair_prompt_includes_error_output() -> None:
    prompt = _build_repair_prompt(_ctx(), _failing_test(), _failed_result(), attempt=1)
    assert "ModuleNotFoundError" in prompt


def test_build_repair_prompt_includes_failing_code() -> None:
    prompt = _build_repair_prompt(_ctx(), _failing_test(), _failed_result(), attempt=1)
    assert "wrong_module" in prompt


def test_build_repair_prompt_includes_function_context() -> None:
    prompt = _build_repair_prompt(_ctx(), _failing_test(), _failed_result(), attempt=1)
    assert "divide" in prompt


def test_build_repair_prompt_does_not_include_full_long_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Long errors are truncated at REPAIR_ERROR_MAX_CHARS."""
    from config.settings import settings

    monkeypatch.setattr(settings, "REPAIR_ERROR_MAX_CHARS", 900)
    long_result = _failed_result(stdout="E " + "x" * 5000)
    prompt = _build_repair_prompt(_ctx(), _failing_test(), long_result, attempt=1)
    assert "x" * 5000 not in prompt
    assert "… (truncado)" in prompt
    assert len(prompt) < 6000