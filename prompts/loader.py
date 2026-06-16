from __future__ import annotations

from pathlib import Path

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def _load_template(name: str) -> str:
    return (_TEMPLATES_DIR / name).read_text(encoding="utf-8").strip()


def build_generator_system_prompt(*, max_test_functions: int, max_lines: int) -> str:
    template = _load_template("generator_system.txt")
    return template.format(max_fn=max_test_functions, max_lines=max_lines)


def load_repair_system_prompt() -> str:
    return _load_template("repair_system.txt")
