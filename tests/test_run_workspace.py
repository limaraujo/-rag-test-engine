from __future__ import annotations

from pathlib import Path

import pytest

from config.run_workspace import RunWorkspace, resolve_workspace_root, source_slug


def test_source_slug_from_named_dir(tmp_path: Path) -> None:
    repo = tmp_path / "meu-projeto"
    repo.mkdir()
    assert source_slug(repo) == "meu-projeto"


def test_source_slug_from_dot_uses_resolved_name(tmp_path: Path) -> None:
    child = tmp_path / "child-repo"
    child.mkdir()
    assert source_slug(child / ".") == "child-repo"


def test_resolve_workspace_without_profile(tmp_path: Path) -> None:
    repo = tmp_path / "mockes"
    repo.mkdir()
    root = resolve_workspace_root(
        repo,
        runs_base=tmp_path / "runs",
        timestamp="20260101_120000",
    )
    assert root == tmp_path / "runs" / "mockes" / "20260101_120000"


def test_resolve_workspace_with_profile(tmp_path: Path) -> None:
    repo = tmp_path / "mockes"
    repo.mkdir()
    root = resolve_workspace_root(
        repo,
        runs_base=tmp_path / "runs",
        profile="rag-completo",
        timestamp="20260101_120000",
    )
    assert root == tmp_path / "runs" / "mockes" / "rag-completo" / "20260101_120000"


def test_resolve_workspace_batch_profiles(tmp_path: Path) -> None:
    repo = tmp_path / "mockes"
    repo.mkdir()
    root = resolve_workspace_root(
        repo,
        runs_base=tmp_path / "runs",
        profile="sem-rag",
        run_group="20260101_120000",
    )
    assert root == tmp_path / "runs" / "mockes" / "20260101_120000" / "sem-rag"


def test_run_workspace_create_with_profile(tmp_path: Path) -> None:
    repo = tmp_path / "app"
    repo.mkdir()
    workspace = RunWorkspace.create(
        repo,
        runs_base=tmp_path / "runs",
        profile="com-cache",
        run_group="batch_001",
    )
    assert workspace.source_slug == "app"
    assert workspace.profile == "com-cache"
    assert workspace.run_group == "batch_001"
    assert workspace.root == tmp_path / "runs" / "app" / "batch_001" / "com-cache"
    assert workspace.logs_dir.is_dir()
    assert workspace.tests_dir.is_dir()
    assert workspace.artifacts_dir.is_dir()
