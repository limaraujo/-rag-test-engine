import platform
import sys
from importlib import import_module
from repositorios.pyjwt.jwt.help import info

# CPython: happy path
def test_info_cpython_happy_path(monkeypatch):
    # Verifica caminho principal: CPython retorna versão de implementação correta
    helpmod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "3.4.7", raising=False)
    monkeypatch.setattr(helpmod, "pyjwt_version", "4.0.0", raising=False)

    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "release", lambda: "5.11.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(platform, "python_version", lambda: "3.11.4")

    info = helpmod.info()
    assert info["platform"] == {"system": "Linux", "release": "5.11.0"}
    assert info["implementation"] == {"name": "CPython", "version": "3.11.4"}
    assert info["cryptography"]["version"] == "3.4.7"
    assert info["pyjwt"]["version"] == "4.0.0"

# PyPy: non-final releaselevel
def test_info_pypy_non_final(monkeypatch):
    # Verifica caminho PyPy com releaselevel não final
    helpmod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "3.2.0", raising=False)
    monkeypatch.setattr(helpmod, "pyjwt_version", "4.1.0", raising=False)

    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "release", lambda: "21.0")
    monkeypatch.setattr(platform, "python_implementation", lambda: "PyPy")
    monkeypatch.setattr(platform, "python_version", lambda: "3.9.0")

    class PypyInfo:
        major = 7
        minor = 3
        micro = 5
        releaselevel = "beta"

    monkeypatch.setattr(sys, "pypy_version_info", PypyInfo, raising=False)

    info = helpmod.info()
    assert info["platform"] == {"system": "Darwin", "release": "21.0"}
    assert info["implementation"] == {"name": "PyPy", "version": "7.3.5beta"}
    assert info["cryptography"]["version"] == "3.2.0"
    assert info["pyjwt"]["version"] == "4.1.0"

# PyPy: final releaselevel
def test_info_pypy_final(monkeypatch):
    # Verifica caminho PyPy com releaselevel final
    helpmod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "3.2.1", raising=False)
    monkeypatch.setattr(helpmod, "pyjwt_version", "4.2.0", raising=False)

    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "release", lambda: "10")
    monkeypatch.setattr(platform, "python_implementation", lambda: "PyPy")
    monkeypatch.setattr(platform, "python_version", lambda: "3.8.6")

    class PypyInfoFinal:
        major = 7
        minor = 3
        micro = 1
        releaselevel = "final"

    monkeypatch.setattr(sys, "pypy_version_info", PypyInfoFinal, raising=False)

    info = helpmod.info()
    assert info["implementation"]["version"] == "7.3.1"

# OSError in platform.system: verify Unknown in platform info
def test_info_platform_oserror(monkeypatch):
    # Verifica path onde falha ao obter informações do sistema
    helpmod = import_module("repositorios.pyjwt.jwt.help")
    monkeypatch.setattr(helpmod, "cryptography_version", "3.5.0", raising=False)
    monkeypatch.setattr(helpmod, "pyjwt_version", "5.0.0", raising=False)

    def raise_oserror():
        raise OSError

    monkeypatch.setattr(platform, "system", raise_oserror)
    monkeypatch.setattr(platform, "release", lambda: "unknown")
    monkeypatch.setattr(platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(platform, "python_version", lambda: "3.10.0")

    info = helpmod.info()
    assert info["platform"] == {"system": "Unknown", "release": "Unknown"}
