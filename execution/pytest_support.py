from __future__ import annotations

import os
import re
from pathlib import Path


def safe_test_stem(target: str) -> str:
    """Normaliza um qualified_name para uso em nomes de arquivo test_*.py."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", target)


def build_pytest_env(extra_pythonpath: list[str]) -> dict[str, str]:
    """Retorna cópia de os.environ com extra_pythonpath no início do PYTHONPATH."""
    env = os.environ.copy()
    if extra_pythonpath:
        existing = env.get("PYTHONPATH", "")
        joined = os.pathsep.join(str(Path(p).resolve()) for p in extra_pythonpath)
        env["PYTHONPATH"] = f"{joined}{os.pathsep}{existing}" if existing else joined
    return env


def pytest_timeout_message(timeout: int) -> str:
    return f"pytest excedeu o tempo limite após {timeout}s"


def parse_pytest_counts(output: str) -> tuple[int, int, int]:
    """
    Analisa a linha de resumo do pytest para extrair contagens de sucesso/falha/erro.

    Lida com linhas como::

        3 passed, 1 failed in 0.42s
        2 passed in 0.10s
        1 error in 0.05s
    """
    passed = failed = errors = 0
    for line in reversed(output.splitlines()):
        if not any(k in line for k in ("passed", "failed", "error")):
            continue
        m = re.search(r"(\d+) passed", line)
        if m:
            passed = int(m.group(1))
        m = re.search(r"(\d+) failed", line)
        if m:
            failed = int(m.group(1))
        m = re.search(r"(\d+) error", line)
        if m:
            errors = int(m.group(1))
        break

    return passed, failed, errors
