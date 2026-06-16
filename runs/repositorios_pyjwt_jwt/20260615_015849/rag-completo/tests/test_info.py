import importlib
import types
from repositorios.pyjwt.jwt.help import info

def _setup_versions(monkeypatch, helpmod):
    monkeypatch.setattr(helpmod, "cryptography_version", "cryptography-1.2.3", raising=False)
    monkeypatch.setattr(helpmod, "pyjwt_version", "4.3.0", raising=False)

def test_info_cpython_happy_path(monkeypatch):
    # CPython path: main branch with explicit versions
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    _setup_versions(monkeypatch, helpmod)
    monkeypatch.setattr(helpmod.platform, "system", lambda: "Linux")
    monkeypatch.setattr(helpmod.platform, "release", lambda: "5.15.0")
    monkeypatch.setattr(helpmod.platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(helpmod.platform, "python_version", lambda: "3.11.2")
    res = helpmod.info()
    assert res == {
        "platform": {"system": "Linux", "release": "5.15.0"},
        "implementation": {"name": "CPython", "version": "3.11.2"},
        "cryptography": {"version": "cryptography-1.2.3"},
        "pyjwt": {"version": "4.3.0"},
    }

def test_info_pypy_non_final_releaselevel(monkeypatch):
    # PyPy path with non-final releaselevel appended to version
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    _setup_versions(monkeypatch, helpmod)
    monkeypatch.setattr(helpmod.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(helpmod.platform, "release", lambda: "20.6.0")
    monkeypatch.setattr(helpmod.platform, "python_implementation", lambda: "PyPy")
    monkeypatch.setattr(helpmod.platform, "python_version", lambda: "3.9.0")
    monkeypatch.setattr(helpmod.sys, "pypy_version_info", types.SimpleNamespace(major=7, minor=3, micro=5, releaselevel="dev"), raising=False)
    res = helpmod.info()
    assert res == {
        "platform": {"system": "Darwin", "release": "20.6.0"},
        "implementation": {"name": "PyPy", "version": "7.3.5dev"},
        "cryptography": {"version": "cryptography-1.2.3"},
        "pyjwt": {"version": "4.3.0"},
    }

def test_info_unknown_implementation(monkeypatch):
    # Unknown implementation triggers Unknown version field
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    _setup_versions(monkeypatch, helpmod)
    monkeypatch.setattr(helpmod.platform, "system", lambda: "Linux")
    monkeypatch.setattr(helpmod.platform, "release", lambda: "1.0")
    monkeypatch.setattr(helpmod.platform, "python_implementation", lambda: "Jython")
    monkeypatch.setattr(helpmod.platform, "python_version", lambda: "2.7")
    res = helpmod.info()
    assert res == {
        "platform": {"system": "Linux", "release": "1.0"},
        "implementation": {"name": "Jython", "version": "Unknown"},
        "cryptography": {"version": "cryptography-1.2.3"},
        "pyjwt": {"version": "4.3.0"},
    }

def test_info_oserror_handles_platform_info(monkeypatch):
    # OSError raised during platform information leads to Unknown platform fields
    helpmod = importlib.import_module("repositorios.pyjwt.jwt.help")
    _setup_versions(monkeypatch, helpmod)
    def raise_oserror():
        raise OSError()
    monkeypatch.setattr(helpmod.platform, "system", raise_oserror)
    monkeypatch.setattr(helpmod.platform, "release", lambda: "x")
    monkeypatch.setattr(helpmod.platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(helpmod.platform, "python_version", lambda: "3.8.1")
    res = helpmod.info()
    assert res["platform"] == {"system": "Unknown", "release": "Unknown"}
    assert res["implementation"] == {"name": "CPython", "version": "3.8.1"}
