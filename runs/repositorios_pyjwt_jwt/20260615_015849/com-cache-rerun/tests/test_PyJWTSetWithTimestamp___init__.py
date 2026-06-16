import time
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# curto: happy path - verifica armazenamento de jwk_set e timestamp a partir de time.monotonic fixado
def test_init_sets_jwk_set_and_timestamp(monkeypatch):
    ts = 123.456
    monkeypatch.setattr(time, "monotonic", lambda: ts)
    dummy = object()
    inst = PyJWTSetWithTimestamp(dummy)
    assert inst.jwk_set is dummy
    assert inst.timestamp == ts

# curto: caso de borda - verifica que qualquer objeto pode ser passado como jwk_set
def test_init_accepts_any_jwk_set_object(monkeypatch):
    ts = 7.89
    monkeypatch.setattr(time, "monotonic", lambda: ts)
    class CustomJWKSet:
        pass
    dummy = CustomJWKSet()
    inst = PyJWTSetWithTimestamp(dummy)
    assert inst.jwk_set is dummy
    assert inst.timestamp == ts
