import importlib
import platform
import sys
import pytest
from types import SimpleNamespace
from repositorios.pyjwt.jwt.help import info

mod = importlib.import_module("repositorios.pyjwt.jwt.help")
info = mod.info

# CPython path: verify platform/implementation/versions for CPython
def test_info_cpython_basic(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "release", lambda: "5.15.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")
    monkeypatch.setattr(mod, "cryptography_version", "40.0.0")
    monkeypatch.setattr(mod, "pyjwt_version", "2.6.0")

    result = info()

    assert result == {
        "platform": {"system": "Linux", "release": "5.15.0"},
        "implementation": {"name": "CPython", "version": "3.11.4"},
        "cryptography": {"version": "40.0.0"},
        "pyjwt": {"version": "2.6.0"},
    }

# PyPy path: final and non-final releaselevel coverage via parameterization
@pytest.mark.parametrize("final", [True, False])
def test_info_pypy_versions(monkeypatch, final):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "release", lambda: "5.15.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "PyPy")
    monkeypatch.setattr(platform, "python_version", lambda: "3.8.0")  # not used for PyPy path
    pypy_version_info = SimpleNamespace(major=7, minor=3, micro=9, releaselevel="final" if final else "beta")
    monkeypatch.setattr(sys, "pypy_version_info", pypy_version_info, raising=False)

    monkeypatch.setattr(mod, "cryptography_version", "40.0.0")
    monkeypatch.setattr(mod, "pyjwt_version", "2.6.0")

    result = info()

    expected_version = "7.3.9" if final else "7.3.9beta"
    assert result == {
        "platform": {"system": "Linux", "release": "5.15.0"},
        "implementation": {"name": "PyPy", "version": expected_version},
        "cryptography": {"version": "40.0.0"},
        "pyjwt": {"version": "2.6.0"},
    }

# OSError path: verify Unknown platform info while still inferring CPython implementation
def test_info_oserror_platform(monkeypatch):
    def raise_oserror():
        raise OSError()

    monkeypatch.setattr(platform, "system", raise_oserror)
    monkeypatch.setattr(platform, "release", lambda: "5.15.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(platform, "python_version", lambda: "3.9.1")
    monkeypatch.setattr(mod, "cryptography_version", "40.0.0")
    monkeypatch.setattr(mod, "pyjwt_version", "2.6.0")

    result = info()

    assert result == {
        "platform": {"system": "Unknown", "release": "Unknown"},
        "implementation": {"name": "CPython", "version": "3.9.1"},
        "cryptography": {"version": "40.0.0"},
        "pyjwt": {"version": "2.6.0"},
    }
