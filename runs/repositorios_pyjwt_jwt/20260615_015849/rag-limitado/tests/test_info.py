import importlib
import platform
import sys
from types import SimpleNamespace
from repositorios.pyjwt.jwt.help import info

# Happy path: CPython on Linux with standard versions
def test_info_happy_path_cpython(monkeypatch):
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "3.4.7")
    monkeypatch.setattr(helpmod, "pyjwt_version", "2.4.0")

    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "release", lambda: "5.15.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.2")

    result = helpmod.info()

    assert result["platform"] == {"system": "Linux", "release": "5.15.0"}
    assert result["implementation"] == {"name": "CPython", "version": "3.11.2"}
    assert result["cryptography"] == {"version": "3.4.7"}
    assert result["pyjwt"] == {"version": "2.4.0"}

# PyPy branch: ensure version formatting from pypy_version_info
def test_info_pyPy_version_format(monkeypatch):
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "3.8.0")
    monkeypatch.setattr(helpmod, "pyjwt_version", "2.5.0")

    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "release", lambda: "22.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "PyPy")
    monkeypatch.setattr(platform, "python_version", lambda: "3.9.1")

    monkeypatch.setattr(sys, "pypy_version_info", SimpleNamespace(major=7, minor=3, micro=5, releaselevel="final"), raising=False)

    result = helpmod.info()

    assert result["platform"] == {"system": "Darwin", "release": "22.0"}
    assert result["implementation"] == {"name": "PyPy", "version": "7.3.5"}
    assert result["cryptography"] == {"version": "3.8.0"}
    assert result["pyjwt"] == {"version": "2.5.0"}

# Unknown implementation: expect version to be "Unknown"
def test_info_unknown_implementation_branch(monkeypatch):
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "1.0.0")
    monkeypatch.setattr(helpmod, "pyjwt_version", "0.9.0")

    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "release", lambda: "10")
    monkeypatch.setattr(platform, "python_implementation", lambda: "IronPython")
    monkeypatch.setattr(platform, "python_version", lambda: "3.8.0")

    result = helpmod.info()

    assert result["implementation"]["name"] == "IronPython"
    assert result["implementation"]["version"] == "Unknown"

# OSError during platform information: ensure Unknown in platform info
def test_info_oserror_in_platform_info(monkeypatch):
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "4.2.0")
    monkeypatch.setattr(helpmod, "pyjwt_version", "3.0.0")

    def raise_oserror():
        raise OSError
    monkeypatch.setattr(platform, "system", raise_oserror)
    monkeypatch.setattr(platform, "release", lambda: "1.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(platform, "python_version", lambda: "3.12.0")

    result = helpmod.info()

    assert result["platform"] == {"system": "Unknown", "release": "Unknown"}
    assert result["implementation"] == {"name": "CPython", "version": "3.12.0"}
