from __future__ import annotations

from agents.policies.repair_policy import skip_repair_reason
from execution.runner import RunResult
from schemas.context import FunctionContext
from tests.conftest import make_symbol


def _ctx(file_path: str = "pkg/calc.py") -> FunctionContext:
    return FunctionContext.from_symbol(
        make_symbol("calc.add", "def add(a, b):\n    return a + b").model_copy(
            update={"file_path": file_path},
        ),
    )


def _result(**kwargs) -> RunResult:
    defaults = dict(
        passed=False,
        exit_code=1,
        stdout="",
        stderr="",
        duration_seconds=0.1,
        test_file="/tmp/test_add.py",
    )
    defaults.update(kwargs)
    return RunResult(**defaults)


def test_skip_collection_error() -> None:
    reason = skip_repair_reason(
        _result(exit_code=2, stdout="ERROR collecting test_foo.py"),
        _ctx(),
    )
    assert reason == "repair_skipped:pytest_collection_error"


def test_skip_setup_error_no_tests_collected() -> None:
    reason = skip_repair_reason(
        _result(num_errors=1, num_passed=0, num_failed=0, stdout="E   SyntaxError"),
        _ctx(),
    )
    assert reason == "repair_skipped:pytest_setup_error"


def test_skip_source_dependency_import() -> None:
    stdout = """\
============================= ERRORS =============================
____________________ ERROR collecting test_calc ____________________
ImportError while importing test module 'test_calc.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
test_calc.py:1: in <module>
    from pkg.calc import add
pkg/calc.py:2: in <module>
    import django
E   ModuleNotFoundError: No module named 'django'
"""
    reason = skip_repair_reason(_result(stdout=stdout, num_errors=1), _ctx())
    assert reason == "repair_skipped:source_import_dependency"


def test_allows_wrong_test_import() -> None:
    stdout = """\
___________________________ test_add ___________________________
test_calc.py:3: in test_add
    from wrong_pkg import add
E   ModuleNotFoundError: No module named 'wrong_pkg'
"""
    reason = skip_repair_reason(
        _result(stdout=stdout, num_failed=1),
        _ctx(),
    )
    assert reason is None


def test_allows_assertion_error() -> None:
    stdout = """\
___________________________ test_add ___________________________
test_calc.py:4: in test_add
    assert add(1, 2) == 99
E   AssertionError: assert 3 == 99
"""
    reason = skip_repair_reason(_result(stdout=stdout, num_failed=1), _ctx())
    assert reason is None
