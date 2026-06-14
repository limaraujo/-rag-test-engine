"""
Limites de chamadas LLM, cobertura e reparo no orchestrator.

Cobre o orçamento por símbolo, parada de loops e isolamento de falhas.
"""
from __future__ import annotations

from textwrap import dedent
from unittest.mock import MagicMock, patch

import pytest

from agents.orchestrator import OrchestratorAgent, _LLMBudget
from agents.repair import RepairAgent
from agents.test_generator import TestGeneratorAgent as GeneratorAgent
from cache.generation_cache import GenerationCache
from config.run_workspace import RunWorkspace
from config.settings import ROOT, settings
from execution.runner import RunResult, TestRunner
from llm.mock_llm import MockLLM
from llm.models import LLMRequest, LLMResponse
from schemas.context import FunctionContext
from schemas.pipeline import PipelineStats, SymbolState
from tests.conftest import make_symbol


_BROKEN_ADD = dedent("""\
    from tests.fixtures.cache_sample.add import add

    def test_add_wrong():
        assert add(1, 2) == 99
""").strip()

_FIXED_ADD = dedent("""\
    from tests.fixtures.cache_sample.add import add

    def test_add_ok():
        assert add(1, 2) == 3
""").strip()


class CountingLLM(MockLLM):
    def __init__(self) -> None:
        super().__init__()
        self.generate_calls = 0

    def generate(self, request: LLMRequest) -> LLMResponse:
        self.generate_calls += 1
        return super().generate(request)


class ScriptedLLM(CountingLLM):
    """LLM determinístico para cenários generate/repair."""

    def __init__(self, *, generate_code: str, repair_code: str | None = None) -> None:
        super().__init__()
        self._generate_code = generate_code
        self._repair_code = repair_code if repair_code is not None else generate_code

    def generate(self, request: LLMRequest) -> LLMResponse:
        self.generate_calls += 1
        if "Arquivo de teste falho" in request.user_prompt:
            content = self._repair_code
        else:
            content = self._generate_code
        return LLMResponse(content=content, model=self.model)


@pytest.fixture
def add_symbol():
    add_path = str((ROOT / "tests" / "fixtures" / "cache_sample" / "add.py").resolve())
    return make_symbol(
        "add",
        source_code="def add(a, b):\n    return a + b",
    ).model_copy(update={"file_path": add_path})


@pytest.fixture
def limits_env(monkeypatch: pytest.MonkeyPatch, tmp_path):
    monkeypatch.setattr(settings, "GENERATION_CACHE_ENABLED", False)
    monkeypatch.setattr(settings, "MAX_COVERAGE_ROUNDS", 0)
    monkeypatch.setattr(settings, "MAX_REPAIRS", 1)
    monkeypatch.setattr(settings, "MAX_LLM_CALLS_PER_SYMBOL", 2)
    monkeypatch.setattr(settings, "COVERAGE_STOP_ON_NO_IMPROVEMENT", True)
    monkeypatch.setattr(settings, "AI_MODE", "offline")
    monkeypatch.setattr(settings, "LOG_API_CALLS", False)
    return tmp_path


def _orchestrator(
    llm: CountingLLM,
    *,
    max_repairs: int | None = None,
) -> OrchestratorAgent:
    repairs = max_repairs if max_repairs is not None else settings.MAX_REPAIRS
    return OrchestratorAgent(
        retriever=MagicMock(
            enrich=lambda ctx, *a, **k: ctx,
        ),
        generator=GeneratorAgent(llm=llm),
        repair_agent=RepairAgent(llm=llm),
        runner=TestRunner(),
        generation_cache=GenerationCache(),
        max_repairs=repairs,
    )


def _run_symbol(
    orchestrator: OrchestratorAgent,
    symbol,
    stats: PipelineStats | None = None,
) -> PipelineStats:
    stats = stats or PipelineStats()
    workspace = RunWorkspace.create(
        ROOT / "tests" / "fixtures" / "cache_sample",
        runs_base=ROOT / "runs" / "_test_limits",
    )
    orchestrator._process_symbol(
        symbol,
        workspace=workspace,
        call_graph=MagicMock(nodes={}),
        dependency_graph=MagicMock(nodes={}),
        symbols_by_name={symbol.qualified_name: symbol},
        source_dir=ROOT,
        pythonpath=[str(ROOT)],
        stats=stats,
    )
    return stats


def test_generation_passes_uses_one_llm_call(limits_env, add_symbol) -> None:
    llm = ScriptedLLM(generate_code=_FIXED_ADD)
    stats = _run_symbol(_orchestrator(llm), add_symbol)

    assert llm.generate_calls == 1
    assert stats.ok == 1
    assert stats.symbol_runs[0].llm_calls == 1
    assert stats.symbol_runs[0].state == SymbolState.COMPLETED


def test_generation_fails_repair_passes_uses_two_calls(limits_env, add_symbol) -> None:
    llm = ScriptedLLM(generate_code=_BROKEN_ADD, repair_code=_FIXED_ADD)
    stats = _run_symbol(_orchestrator(llm), add_symbol)

    assert llm.generate_calls == 2
    assert stats.ok == 1
    assert stats.repaired == 1
    assert stats.symbol_runs[0].llm_calls == 2


def test_llm_budget_blocks_third_call(limits_env, add_symbol) -> None:
    llm = ScriptedLLM(generate_code=_BROKEN_ADD, repair_code=_BROKEN_ADD)
    stats = _run_symbol(_orchestrator(llm, max_repairs=3), add_symbol)

    assert llm.generate_calls == 2
    assert stats.failed == 1
    assert stats.symbol_runs[0].stop_reason in {
        "llm_budget_exhausted",
        "same_error_repeated",
        "tests_failed",
    }


def test_coverage_disabled_no_regeneration(limits_env, add_symbol, monkeypatch) -> None:
    monkeypatch.setattr(settings, "MAX_COVERAGE_ROUNDS", 0)
    llm = ScriptedLLM(generate_code=_FIXED_ADD)
    with patch.object(OrchestratorAgent, "_coverage_loop", wraps=OrchestratorAgent._coverage_loop) as cov:
        stats = _run_symbol(_orchestrator(llm), add_symbol)
        cov.assert_called_once()
    assert llm.generate_calls == 1
    assert stats.coverage_boosted == 0


def test_coverage_stops_when_no_improvement(limits_env, add_symbol, monkeypatch) -> None:
    monkeypatch.setattr(settings, "MAX_COVERAGE_ROUNDS", 3)
    llm = ScriptedLLM(generate_code=_FIXED_ADD)

    summaries = [
        {
            "line_coverage_percent": 50.0,
            "threshold_percent": 80.0,
            "meets_threshold": False,
            "missing_lines": [3],
            "gaps": [{"function_name": "add", "uncovered_lines": [3]}],
        },
        {
            "line_coverage_percent": 50.0,
            "threshold_percent": 80.0,
            "meets_threshold": False,
            "missing_lines": [4],
            "gaps": [{"function_name": "add", "uncovered_lines": [4]}],
        },
    ]

    class FakeAnalyzer:
        def __init__(self, *a, **k) -> None:
            pass

        def run(self):
            return RunResult(passed=True, exit_code=0, stdout="", stderr="", duration_seconds=0.0, test_file="t.py")

        def generate_summary(self):
            return summaries.pop(0) if summaries else summaries[-1]

        def gaps_for_prompt(self):
            return []

    monkeypatch.setattr("agents.orchestrator.CoverageAnalyzer", FakeAnalyzer)
    stats = _run_symbol(_orchestrator(llm), add_symbol)

    assert llm.generate_calls == 2
    assert stats.symbol_runs[0].stop_reason == "coverage_no_improvement"


def test_coverage_stops_at_threshold(limits_env, add_symbol, monkeypatch) -> None:
    monkeypatch.setattr(settings, "MAX_COVERAGE_ROUNDS", 2)
    llm = ScriptedLLM(generate_code=_FIXED_ADD)

    summaries = [
        {"line_coverage_percent": 60.0, "threshold_percent": 80.0, "meets_threshold": False,
         "missing_lines": [3], "gaps": [{"function_name": "add", "uncovered_lines": [3]}]},
        {"line_coverage_percent": 85.0, "threshold_percent": 80.0, "meets_threshold": True,
         "missing_lines": [], "gaps": []},
    ]

    class FakeAnalyzer:
        def __init__(self, *a, **k) -> None:
            pass

        def run(self):
            return RunResult(passed=True, exit_code=0, stdout="", stderr="", duration_seconds=0.0, test_file="t.py")

        def generate_summary(self):
            return summaries.pop(0)

        def gaps_for_prompt(self):
            return []

    monkeypatch.setattr("agents.orchestrator.CoverageAnalyzer", FakeAnalyzer)
    stats = _run_symbol(_orchestrator(llm), add_symbol)

    assert llm.generate_calls == 2
    assert stats.ok == 1


def test_same_error_repeated_skips_repair_loop(limits_env, add_symbol) -> None:
    llm = ScriptedLLM(generate_code=_BROKEN_ADD, repair_code=_BROKEN_ADD)
    stats = _run_symbol(_orchestrator(llm, max_repairs=2), add_symbol)

    assert llm.generate_calls == 2
    assert stats.symbol_runs[0].stop_reason == "same_error_repeated"


def test_one_symbol_failure_does_not_block_others(limits_env, monkeypatch) -> None:
    add_path = str((ROOT / "tests" / "fixtures" / "cache_sample" / "add.py").resolve())
    sym_ok = make_symbol("add", source_code="def add(a, b):\n    return a + b").model_copy(
        update={"file_path": add_path},
    )
    sym_fail = make_symbol("sub", source_code="def sub(a, b):\n    return a - b").model_copy(
        update={"file_path": add_path.replace("add.py", "sub.py")},
    )

    class MultiLLM(CountingLLM):
        def generate(self, request: LLMRequest) -> LLMResponse:
            self.generate_calls += 1
            if "sub" in request.label:
                content = _BROKEN_ADD.replace("add", "sub")
            elif "Arquivo de teste falho" in request.user_prompt:
                content = _BROKEN_ADD.replace("add", "sub")
            else:
                content = _FIXED_ADD
            return LLMResponse(content=content, model=self.model)

    llm = MultiLLM()
    orchestrator = _orchestrator(llm, max_repairs=1)
    stats = PipelineStats()

    _run_symbol(orchestrator, sym_fail, stats)
    _run_symbol(orchestrator, sym_ok, stats)

    assert stats.failed == 1
    assert stats.ok == 1
    assert len(stats.symbol_runs) == 2


def test_llm_budget_dataclass() -> None:
    budget = _LLMBudget(max_calls=2)
    assert budget.record("generate")
    assert budget.record("repair_1")
    assert not budget.can_call()
    assert budget.calls == 2
