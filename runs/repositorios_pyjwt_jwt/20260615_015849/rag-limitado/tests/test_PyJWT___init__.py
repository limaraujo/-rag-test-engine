import importlib
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# short
# happy path: sem argumentos; usa default options e instancia PyJWS com sig_options
def test_pyjwt_init_without_explicit_options(monkeypatch):
    api_module = importlib.import_module("repositorios.pyjwt.jwt.api_jwt")

    class DummyPyJWS:
        instances = []
        def __init__(self, *, options=None, **kwargs):
            DummyPyJWS.instances.append(self)
            self.options = options

    monkeypatch.setattr(api_module, "PyJWS", DummyPyJWS)

    monkeypatch.setattr(api_module.PyJWT, "_get_default_options", lambda self: {"default": True})
    monkeypatch.setattr(api_module.PyJWT, "_get_sig_options", lambda self: {"sig": "sentinel"})

    merge_calls = []
    def _merge_options_impl(self, options):
        merge_calls.append(options)
        return {"merged": options}
    monkeypatch.setattr(api_module.PyJWT, "_merge_options", _merge_options_impl)

    jwt = api_module.PyJWT()

    assert jwt.options == {"default": True}
    assert merge_calls == []
    assert DummyPyJWS.instances[0].options == {"sig": "sentinel"}


# short
# with options: verifica que _merge_options é chamado e PyJWS recebe sig_options
def test_pyjwt_init_with_explicit_options(monkeypatch):
    api_module = importlib.import_module("repositorios.pyjwt.jwt.api_jwt")

    class DummyPyJWS:
        instances = []
        def __init__(self, *, options=None, **kwargs):
            DummyPyJWS.instances.append(self)
            self.options = options

    monkeypatch.setattr(api_module, "PyJWS", DummyPyJWS)

    monkeypatch.setattr(api_module.PyJWT, "_get_default_options", lambda self: {"default": True})
    monkeypatch.setattr(api_module.PyJWT, "_get_sig_options", lambda self: {"sig": "sentinel2"})

    merge_calls = []
    def _merge_options_impl(self, options):
        merge_calls.append(options)
        return {"merged": options}
    monkeypatch.setattr(api_module.PyJWT, "_merge_options", _merge_options_impl)

    jwt = api_module.PyJWT(options={"foo": "bar"})

    assert jwt.options == {"merged": {"foo": "bar"}}
    assert merge_calls == [{"foo": "bar"}]
    assert DummyPyJWS.instances[0].options == {"sig": "sentinel2"}
