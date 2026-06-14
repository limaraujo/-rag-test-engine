from __future__ import annotations

from dataclasses import dataclass, field

from config.run_workspace import RunWorkspace
from execution.runner import SuiteValidationResult


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
