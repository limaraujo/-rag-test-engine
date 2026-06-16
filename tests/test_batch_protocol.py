from __future__ import annotations

from pathlib import Path

from scripts.compare_run_metrics import build_cache_benchmark, profile_summary
from scripts.run_all_profiles import fair_batch_steps, legacy_batch_steps


def test_fair_batch_clears_cache_after_rag_not_after_first_com_cache() -> None:
    steps = {s.profile: s.clear_cache_after for s in fair_batch_steps()}
    assert steps["sem-rag"] is True
    assert steps["rag-limitado"] is True
    assert steps["rag-completo"] is True
    assert steps["com-cache"] is False
    assert steps["com-cache-rerun"] is True


def test_legacy_batch_clears_after_every_cli_profile() -> None:
    steps = legacy_batch_steps()
    assert all(s.clear_cache_after for s in steps)
    assert len(steps) == 4


def test_build_cache_benchmark_from_summaries() -> None:
    cold = profile_summary(
        {
            "rates": {"valid_generation_percent": 80, "first_attempt_success_percent": 70, "approval_percent": 100},
            "coverage": {"symbol_line_avg_percent": 90, "symbol_branch_avg_percent": 85},
            "cost": {"total_tokens": 1000, "total_llm_calls": 50},
            "performance": {"avg_duration_seconds_per_symbol": 10},
            "productivity": {"valid_tests_saved_per_llm_call": 0.5},
            "symbols_processed": 10,
            "symbols_executable": 9,
            "symbols_saved": 8,
            "symbols_failed": 2,
            "per_symbol": [],
        },
        run_summary={"stats": {"generation_cache": {"hits": 0, "misses": 10}}},
    )
    warm = profile_summary(
        {
            "rates": {"valid_generation_percent": 80, "first_attempt_success_percent": 90, "approval_percent": 100},
            "coverage": {"symbol_line_avg_percent": 90, "symbol_branch_avg_percent": 85},
            "cost": {"total_tokens": 200, "total_llm_calls": 5},
            "performance": {"avg_duration_seconds_per_symbol": 2},
            "productivity": {"valid_tests_saved_per_llm_call": 1.6},
            "symbols_processed": 10,
            "symbols_executable": 9,
            "symbols_saved": 8,
            "symbols_failed": 2,
            "per_symbol": [],
        },
        run_summary={
            "stats": {
                "generation_cache": {
                    "hits": 8,
                    "misses": 2,
                    "llm_calls_avoided": 8,
                }
            }
        },
    )
    bench = build_cache_benchmark({"com-cache": cold, "com-cache-rerun": warm})
    assert bench is not None
    assert bench["token_reduction_percent"] == 80.0
    assert bench["warm_cache_hits"] == 8
    assert bench["warm_llm_calls_avoided"] == 8
