from __future__ import annotations

import json
import subprocess
from pathlib import Path
from textwrap import dedent

import pytest

from config.security_paths import audit_tracked_files, is_sensitive_path
from config.settings import ROOT, settings
from config.source_guard import SourceDirBlockedError, ensure_source_dir_allowed, validate_source_dir
from parsers.source.path_filters import scan_python_files
from llm.call_logger import APICallLogger
from llm.models import LLMRequest, LLMResponse
from llm.sanitize import sanitize_text


def _write(path: Path, content: str = "x = 1\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def _git_tracked_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


@pytest.fixture
def small_project(tmp_path: Path) -> Path:
    root = tmp_path / "small_app"
    root.mkdir()
    _write(root / "src" / "calc.py", "def add(a, b):\n    return a + b")
    _write(root / ".env", "SECRET=must-not-be-read")
    _write(root / ".env.local", "TOKEN=also-secret")
    _write(root / "secrets" / "keys.py", "KEY = 'hidden'")
    _write(root / "notes.md", "# docs")
    return root


def test_env_files_never_discovered(small_project: Path) -> None:
    result = scan_python_files(small_project)
    names = {p.name for p in result.files}
    rel_names = {
        p.resolve().relative_to(small_project.resolve()).as_posix()
        for p in result.files
    }

    assert ".env" not in names
    assert ".env.local" not in names
    assert "secrets/keys.py" not in rel_names
    assert "src/calc.py" in rel_names


def test_sensitive_paths_flagged(small_project: Path) -> None:
    assert is_sensitive_path(small_project / ".env", small_project)
    assert is_sensitive_path(small_project / "secrets" / "keys.py", small_project)
    assert not is_sensitive_path(small_project / "src" / "calc.py", small_project)


def test_secret_masked_in_api_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from config import settings as settings_module

    monkeypatch.setattr(settings_module.settings, "LOG_API_CALL_BODIES", True)

    logger = APICallLogger()
    logger.configure(tmp_path)
    logger.reset()

    secret = "sk-" + ("abcdefghijklmnopqrstuvwxyz1234567890")
    bearer = "Bearer " + ("abcdefghijklmnopqrstuvwxyz12345")
    request = LLMRequest(
        system_prompt="system",
        user_prompt=f"token {bearer} in context",
        agent="test_generator",
    )
    response = LLMResponse(content=f"reply uses {secret}", model="mock")

    path = logger.log_llm(request, response, model="mock")
    assert path is not None
    payload = json.loads(path.read_text(encoding="utf-8"))
    blob = json.dumps(payload)

    assert secret not in blob
    assert "sk-***" in blob
    assert "Bearer ***" in blob


def test_sanitize_does_not_alter_normal_source_code() -> None:
    code = dedent("""\
        def add(a: int, b: int) -> int:
            return a + b

        class Calculator:
            def multiply(self, x: int, y: int) -> int:
                return x * y
    """)
    assert sanitize_text(code) == code


def test_source_dir_root_emits_warning(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setattr(settings, "SOURCE_DIR_STRICT", False)
    caplog.set_level("WARNING")

    validation = validate_source_dir(ROOT, allow_risky=False)

    assert not validation.blocked
    assert any("raiz do RAG test engine" in w for w in validation.warnings)
    assert any("raiz do RAG test engine" in r.message for r in caplog.records)


def test_strict_mode_blocks_engine_root(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "SOURCE_DIR_STRICT", True)
    monkeypatch.setattr(settings, "SOURCE_DIR_ALLOW_RISKY", False)

    with pytest.raises(SourceDirBlockedError):
        ensure_source_dir_allowed(ROOT, allow_risky=False)


def test_strict_mode_allows_with_explicit_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "SOURCE_DIR_STRICT", True)

    validation = ensure_source_dir_allowed(ROOT, allow_risky=True)
    assert not validation.blocked


def test_small_directory_runs_without_block(
    small_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "SOURCE_DIR_STRICT", False)
    monkeypatch.setattr(settings, "SOURCE_DIR_PY_WARN_THRESHOLD", 200)

    validation = ensure_source_dir_allowed(small_project)
    assert not validation.blocked
    assert validation.warnings == ()


def test_log_api_call_bodies_disabled_by_default() -> None:
    assert settings.LOG_API_CALL_BODIES is False


def test_no_real_secrets_in_tracked_files() -> None:
    tracked = _git_tracked_files(ROOT)
    if not tracked:
        pytest.skip("repositório git indisponível")

    risks = audit_tracked_files(ROOT, tracked)
    real_risks = [
        r for r in risks
        if r.risk_type not in {"tracked_env_file"}
        and not (r.risk_type == "openai_api_key" and r.path.endswith(".env.example"))
    ]
    assert real_risks == [], (
        "Segredos detectados em arquivos versionados: "
        + ", ".join(f"{r.path} ({r.risk_type})" for r in real_risks)
    )


def test_tracked_env_files_reported_without_values() -> None:
    tracked = _git_tracked_files(ROOT)
    if not tracked:
        pytest.skip("repositório git indisponível")

    env_risks = [r for r in audit_tracked_files(ROOT, tracked) if r.risk_type == "tracked_env_file"]
    assert all(r.path != ".env" for r in env_risks)
