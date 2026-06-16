import pytest
from importlib import import_module
from repositorios.pyjwt.jwt.help import info

# CPython: happy path
def test_info_cpython_happy_path(monkeypatch):
    # Verifica caminho principal: CPython retorna versão de implementação correta
    mod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(mod, "cryptography_version", "3.4.7", raising=False)
    monkeypatch.setattr(mod, "pyjwt_version", "2.5.0", raising=False)

    monkeypatch.setattr(mod.platform, "system", lambda: "Linux", raising=True)
    monkeypatch.setattr(mod.platform, "release", lambda: "5.15.0", raising=True)
    monkeypatch.setattr(mod.platform, "python_implementation", lambda: "CPython", raising=True)
    monkeypatch.setattr(mod.platform, "python_version", lambda: "3.11.2", raising=True)

    info = mod.info()
    assert info == {
        "platform": {"system": "Linux", "release": "5.15.0"},
        "implementation": {"name": "CPython", "version": "3.11.2"},
        "cryptography": {"version": "3.4.7"},
        "pyjwt": {"version": "2.5.0"},
    }

# PyPy: versão com releaselevel não final
def test_info_pypy_with_prerelease(monkeypatch):
    # Verifica o caminho PyPy com releaselevel diferente de final
    mod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(mod, "cryptography_version", "3.4.7", raising=False)
    monkeypatch.setattr(mod, "pyjwt_version", "2.5.0", raising=False)

    monkeypatch.setattr(mod.platform, "python_implementation", lambda: "PyPy", raising=True)
    monkeypatch.setattr(mod.platform, "system", lambda: "FreeBSD", raising=True)
    monkeypatch.setattr(mod.platform, "release", lambda: "12.0", raising=True)

    class PyPyInfo:
        pass
    py_info = PyPyInfo()
    py_info.major = 7
    py_info.minor = 3
    py_info.micro = 9
    py_info.releaselevel = "beta"

    monkeypatch.setattr(mod.sys, "pypy_version_info", py_info, raising=False)

    info = mod.info()
    assert info == {
        "platform": {"system": "FreeBSD", "release": "12.0"},
        "implementation": {"name": "PyPy", "version": "7.3.9beta"},
        "cryptography": {"version": "3.4.7"},
        "pyjwt": {"version": "2.5.0"},
    }

# OSError ao coletar informações de plataforma
def test_info_platform_info_raises_oserror(monkeypatch):
    # Verifica exceção: quando OSError ocorre, usa Unknown
    mod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(mod, "cryptography_version", "3.4.7", raising=False)
    monkeypatch.setattr(mod, "pyjwt_version", "2.5.0", raising=False)

    def raise_oserror():
        raise OSError
    monkeypatch.setattr(mod.platform, "system", raise_oserror, raising=True)

    monkeypatch.setattr(mod.platform, "python_implementation", lambda: "CPython", raising=True)
    monkeypatch.setattr(mod.platform, "python_version", lambda: "3.9.1", raising=True)

    info = mod.info()
    assert info["platform"] == {"system": "Unknown", "release": "Unknown"}
    assert info["implementation"] == {"name": "CPython", "version": "3.9.1"}
    assert info["cryptography"]["version"] == "3.4.7"
    assert info["pyjwt"]["version"] == "2.5.0"

# Outro caminho de implementação: Unknown version
def test_info_unknown_implementation_path(monkeypatch):
    # Verifica caminho onde a implementação não é CPython nem PyPy
    mod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(mod, "cryptography_version", "3.4.7", raising=False)
    monkeypatch.setattr(mod, "pyjwt_version", "2.5.0", raising=False)

    monkeypatch.setattr(mod.platform, "python_implementation", lambda: "Jython", raising=True)
    monkeypatch.setattr(mod.platform, "system", lambda: "Linux", raising=True)
    monkeypatch.setattr(mod.platform, "release", lambda: "1.0", raising=True)
    monkeypatch.setattr(mod.platform, "python_version", lambda: "2.7.2", raising=True)

    info = mod.info()
    assert info["implementation"] == {"name": "Jython", "version": "Unknown"}
