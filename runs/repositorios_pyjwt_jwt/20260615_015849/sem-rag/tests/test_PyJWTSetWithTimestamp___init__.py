import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# happy path: verifica que jwk_set é armazenado e timestamp recebe o valor de time.monotonic
def test_init_stores_jwk_and_timestamp_happy_path(monkeypatch):
    dummy = object()
    monkeypatch.setattr('repositorios.pyjwt.jwt.api_jwk.time.monotonic', lambda: 123.456)
    instance = PyJWTSetWithTimestamp(dummy)
    assert instance.jwk_set is dummy
    assert instance.timestamp == 123.456

# identity reference: verifica que o objeto passado é armazenado pela referência
def test_init_stores_same_object_reference(monkeypatch):
    orig = []
    monkeypatch.setattr('repositorios.pyjwt.jwt.api_jwk.time.monotonic', lambda: 0.0)
    instance = PyJWTSetWithTimestamp(orig)
    assert instance.jwk_set is orig
