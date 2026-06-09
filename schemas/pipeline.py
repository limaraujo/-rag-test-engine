from __future__ import annotations

from dataclasses import dataclass, field

from config.run_workspace import RunWorkspace


@dataclass
class PipelineStats:
    ok: int = 0
    repaired: int = 0
    failed: int = 0
    skipped: int = 0
    coverage_boosted: int = 0

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
