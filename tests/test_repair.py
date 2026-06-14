"""
Testa a função _build_repair_prompt de agents/repair.py.

ESCOPO: apenas a construção do prompt — sem LLM, sem mock de API.

_build_repair_prompt é uma função pura que monta o texto enviado ao LLM
quando um teste falha. Testá-la garante que o LLM recebe as informações
certas (contexto, código falhando, erro do pytest) sem depender de API.

O que NÃO está aqui (e por quê):
  - Testes de RepairAgent.repair() com LLM mockado foram removidos.
    A classe só orquestra: chama o LLM e repassa para _parse_response
    (que já é exercido pelos testes de test_test_generator.py).
    Testar um mock não valida que o repair funciona de verdade.
"""
from __future__ import annotations

from agents.repair import _build_repair_prompt
from execution.runner import RunResult
from schemas.context import FunctionContext
from schemas.outputs import GeneratedTest
from tests.conftest import make_symbol


# ── Fixtures inline (sem pytest.fixture para manter o arquivo simples) ────────

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


# ── _build_repair_prompt ──────────────────────────────────────────────────────

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


def test_build_repair_prompt_does_not_include_full_long_error() -> None:
    """Erros muito longos devem ser cortados para não estourar o contexto do LLM."""
    long_result = _failed_result(stdout="E " + "x" * 5000)
    prompt = _build_repair_prompt(_ctx(), _failing_test(), long_result, attempt=1)
    assert "x" * 5000 not in prompt
    assert len(prompt) < 12_000