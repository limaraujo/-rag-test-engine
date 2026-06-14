from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from config.run_workspace import RunWorkspace
from execution.runner import SuiteValidationResult


class SymbolState(str, Enum):
    """Estado explícito do pipeline por símbolo."""

    GENERATED = "generated"
    TEST_FAILED = "test_failed"
    REPAIRING = "repairing"
    PASSED = "passed"
    COVERAGE_CHECKED = "coverage_checked"
    COVERAGE_STALLED = "coverage_stalled"
    COMPLETED = "completed"


@dataclass
class SymbolRunRecord:
    qualified_name: str
    state: SymbolState = SymbolState.GENERATED
    llm_calls: int = 0
    stop_reason: str | None = None
    previous_coverage_percent: float | None = None
    current_coverage_percent: float | None = None
    repaired: bool = False
    coverage_boosted: bool = False
    passed: bool = False
    from_cache: bool = False

    def set_state(self, state: SymbolState) -> None:
        self.state = state

    def to_dict(self) -> dict:
        return {
            "qualified_name": self.qualified_name,
            "state": self.state.value,
            "llm_calls": self.llm_calls,
            "stop_reason": self.stop_reason,
            "previous_coverage_percent": self.previous_coverage_percent,
            "current_coverage_percent": self.current_coverage_percent,
            "repaired": self.repaired,
            "coverage_boosted": self.coverage_boosted,
            "passed": self.passed,
            "from_cache": self.from_cache,
        }


@dataclass
class GenerationCacheStats:
    hits: int = 0
    misses: int = 0
    stale: int = 0
    invalidations: int = 0
    llm_calls_avoided: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "stale": self.stale,
            "invalidations": self.invalidations,
            "llm_calls_avoided": self.llm_calls_avoided,
        }


@dataclass
class PipelineStats:
    ok: int = 0
    repaired: int = 0
    failed: int = 0
    skipped: int = 0
    coverage_boosted: int = 0
    generation_cache: GenerationCacheStats = field(default_factory=GenerationCacheStats)
    symbol_runs: list[SymbolRunRecord] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.ok + self.failed + self.skipped


@dataclass
class OrchestrationResult:
    workspace: RunWorkspace
    stats: PipelineStats
    indexed: int = 0
    cache_hits: int = 0
    token_summary: str | None = None
    validation: SuiteValidationResult | None = None
    generation_cache: GenerationCacheStats | None = None
