import repositorios.pyjwt.jwt.api_jwk as api_jwk
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# verificação: happy path de atribuição do jwk_set
def test_init_stores_jwk_set(monkeypatch):
    dummy = object()
    obj = PyJWTSetWithTimestamp(dummy)
    assert obj.jwk_set is dummy

# verificação: timestamp é definido usando time.monotonic() durante a inicialização
def test_init_sets_timestamp_using_monotonic(monkeypatch):
    dummy = object()
    monkeypatch.setattr(api_jwk.time, "monotonic", lambda: 123.456)
    obj = PyJWTSetWithTimestamp(dummy)
    assert obj.timestamp == 123.456
