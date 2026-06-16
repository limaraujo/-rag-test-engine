import pytest
import repositorios.pyjwt.jwt.api_jwt as api_jwt
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# Verifica caminho sem opções: usa opções padrão e cria PyJWS com sig_opts
def test_init_without_options_uses_defaults_and_creates_jws(monkeypatch):
    default_opts = {'a': 1}
    sig_opts = {'sig': 'ok'}
    calls = []

    def fake_get_default_options(self):
        calls.append('_get_default_options')
        return default_opts

    def fake_get_sig_options(self):
        calls.append('_get_sig_options')
        return sig_opts

    class DummyPyJWS:
        last_init_options = None
        def __init__(self, *, options):
            DummyPyJWS.last_init_options = options

    monkeypatch.setattr(api_jwt.PyJWT, '_get_default_options', fake_get_default_options, raising=True)
    monkeypatch.setattr(api_jwt.PyJWT, '_get_sig_options', fake_get_sig_options, raising=True)
    monkeypatch.setattr(api_jwt, 'PyJWS', DummyPyJWS)

    jwt = api_jwt.PyJWT()

    assert jwt.options == default_opts
    assert DummyPyJWS.last_init_options == sig_opts
    assert calls == ['_get_default_options', '_get_sig_options']

# Verifica caminho com opções: options são mescladas e PyJWS recebe sig_opts
def test_init_with_options_merges_and_builds_jws(monkeypatch):
    options_input = {'foo': 'bar'}
    default_opts = {'a': 1}
    merged_opts = {'a': 2, 'foo': 'bar'}
    sig_opts = {'sig': 'baz'}
    calls = []

    def fake_get_default_options(self):
        calls.append('_get_default_options')
        return default_opts

    def fake_merge_options(self, options):
        calls.append('_merge_options')
        assert options is options_input
        return merged_opts

    def fake_get_sig_options(self):
        calls.append('_get_sig_options')
        return sig_opts

    class DummyPyJWS:
        last_init_options = None
        def __init__(self, *, options):
            DummyPyJWS.last_init_options = options

    monkeypatch.setattr(api_jwt.PyJWT, '_get_default_options', fake_get_default_options, raising=True)
    monkeypatch.setattr(api_jwt.PyJWT, '_merge_options', fake_merge_options, raising=True)
    monkeypatch.setattr(api_jwt.PyJWT, '_get_sig_options', fake_get_sig_options, raising=True)
    monkeypatch.setattr(api_jwt, 'PyJWS', DummyPyJWS)

    jwt = api_jwt.PyJWT(options=options_input)

    assert jwt.options == merged_opts
    assert DummyPyJWS.last_init_options == sig_opts
    assert calls == ['_get_default_options', '_merge_options', '_get_sig_options']
