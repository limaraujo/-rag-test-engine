from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from config.settings import settings
from parsers.source.dependency_graph import DependencyGraphBuilder
from parsers.source.path_filters import (
    DEFAULT_SKIP_DIRS,
    DEFAULT_SKIP_FILE_GLOBS,
    get_skip_dirs,
    get_skip_file_globs,
    scan_python_files,
)
from parsers.source.scanner import RepositoryScanner


def _write(path: Path, content: str = "x = 1\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def _fixture_tree(root: Path) -> None:
    _write(root / "src" / "foo.py", "def foo(): return 1")
    _write(root / "app" / "bar.py", "def bar(): return 2")
    _write(root / "lib" / "baz.py", "def baz(): return 3")
    _write(root / "tests" / "test_foo.py", "def test_foo(): assert True")
    _write(root / "runs" / "old_run" / "tests" / "test_main.py", "def test_main(): pass")
    _write(root / "test_alpha.py", "def test_alpha(): pass")
    _write(root / "alpha_test.py", "def run(): pass")
    _write(root / "conftest.py", "import pytest")
    _write(root / "mockes" / "embedding_demo.py", "def demo(): pass")
    _write(root / ".env", "SECRET=must-not-be-read")
    _write(root / "notes.md", "# not python")
    _write(root / "__pycache__" / "foo.cpython-312.pyc", "bytecode")


@pytest.fixture
def sample_project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    root.mkdir()
    _fixture_tree(root)
    return root


def _included_names(root: Path, files: tuple[Path, ...]) -> set[str]:
    return {path.resolve().relative_to(root.resolve()).as_posix() for path in files}


def test_tests_directory_ignored(sample_project: Path) -> None:
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert "tests/test_foo.py" not in names
    assert "src/foo.py" in names


def test_runs_directory_ignored(sample_project: Path) -> None:
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert not any(name.startswith("runs/") for name in names)


def test_test_file_globs_ignored(sample_project: Path) -> None:
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert "test_alpha.py" not in names
    assert "alpha_test.py" not in names
    assert "conftest.py" not in names


def test_src_app_lib_included(sample_project: Path) -> None:
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert "src/foo.py" in names
    assert "app/bar.py" in names
    assert "lib/baz.py" in names


def test_demo_glob_still_ignored(sample_project: Path) -> None:
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert "mockes/embedding_demo.py" not in names


def test_non_python_files_not_discovered(sample_project: Path) -> None:
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert ".env" not in names
    assert "notes.md" not in names
    assert "__pycache__/foo.cpython-312.pyc" not in names


def test_secrets_directory_ignored(sample_project: Path) -> None:
    _write(sample_project / "secrets" / "vault.py", "TOKEN = 'hidden'")
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert "secrets/vault.py" not in names


def test_exclusions_reduce_file_count(sample_project: Path) -> None:
    result = scan_python_files(sample_project)
    assert result.total_py_found > result.included
    assert result.excluded >= 5
    assert result.included == 3


def test_configurable_skip_dirs_respected(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write(sample_project / "custom_skip" / "skip_me.py")
    _write(sample_project / "custom_skip" / "keep" / "keep_me.py")

    monkeypatch.setattr(settings, "INGEST_SKIP_DIRS", "custom_skip")
    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)

    assert "custom_skip/skip_me.py" not in names
    assert "custom_skip/keep/keep_me.py" not in names
    assert "src/foo.py" in names


def test_configurable_skip_globs_merged_with_defaults(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write(sample_project / "src" / "legacy_old.py")
    monkeypatch.setattr(settings, "INGEST_SKIP_FILE_GLOBS", "legacy_*.py")

    globs = get_skip_file_globs()
    assert "test_*.py" in globs
    assert "legacy_*.py" in globs

    result = scan_python_files(sample_project)
    names = _included_names(sample_project, result.files)
    assert "src/legacy_old.py" not in names
    assert "test_alpha.py" not in names


def test_defaults_not_removed_by_empty_env() -> None:
    assert "tests" in get_skip_dirs()
    assert "runs" in get_skip_dirs()
    assert DEFAULT_SKIP_DIRS <= get_skip_dirs()
    assert set(DEFAULT_SKIP_FILE_GLOBS) <= set(get_skip_file_globs())


def test_scanner_and_dependency_graph_same_files(sample_project: Path) -> None:
    scanner_files = {
        path.resolve().relative_to(sample_project.resolve()).as_posix()
        for path in RepositoryScanner(str(sample_project)).scan_repository()
    }
    graph_files = {
        path.resolve().relative_to(sample_project.resolve()).as_posix()
        for path in DependencyGraphBuilder(str(sample_project))._discover_python_files()
    }
    assert scanner_files == graph_files


def test_windows_style_root_normalized(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _write(root / "src" / "module.py")
    _write(root / "tests" / "test_module.py")

    result = scan_python_files(str(root))
    names = _included_names(root, result.files)
    assert "src/module.py" in names
    assert "tests/test_module.py" not in names
