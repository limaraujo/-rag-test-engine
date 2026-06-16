import pytest
from importlib import import_module
from repositorios.pyjwt.jwt.api_jwt import PyJWT

api_jwt = import_module("repositorios.pyjwt.jwt.api_jwt")


# short: happy path - without explicit options, default options are used and PyJWS is instantiated with _get_sig_options
def test_init_uses_default_options_and_builds_jws_without_options(monkeypatch):
    class DummyPyJWS:
        last_instance = None
        def __init__(self, *, options=None):
            self.options = options
            DummyPyJWS.last_instance = self

    monkeypatch.setattr(api_jwt, "PyJWS", DummyPyJWS, raising=True)
    monkeypatch.setattr(PyJWT, "_get_default_options", lambda self: {"default": True})
    monkeypatch.setattr(PyJWT, "_get_sig_options", lambda self: {"sig": "X"})
    def raise_if_called(self, options):
        raise AssertionError("merge_options should not be called when no options are provided")
    monkeypatch.setattr(PyJWT, "_merge_options", raise_if_called, raising=True)

    jwt = PyJWT()
    assert jwt.options == {"default": True}
    assert DummyPyJWS.last_instance is not None
    assert DummyPyJWS.last_instance.options == {"sig": "X"}


# short: provided options trigger _merge_options and still initialize PyJWS with _get_sig_options
def test_init_with_options_calls_merge_and_builds_jws(monkeypatch):
    class DummyPyJWS:
        last_instance = None
        def __init__(self, *, options=None):
            self.options = options
            DummyPyJWS.last_instance = self

    monkeypatch.setattr(api_jwt, "PyJWS", DummyPyJWS, raising=True)
    monkeypatch.setattr(PyJWT, "_get_sig_options", lambda self: {"sig": 123})
    monkeypatch.setattr(PyJWT, "_merge_options", lambda self, options: {"merged": True}, raising=True)

    jwt = PyJWT(options={"foo": "bar"})
    assert jwt.options == {"merged": True}
    assert DummyPyJWS.last_instance is not None
    assert DummyPyJWS.last_instance.options == {"sig": 123}
