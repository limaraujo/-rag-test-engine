import pytest
import repositorios.pyjwt.jwt.jwk_set_cache as jwk_set_cache_module
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

def test_put_non_none_stores_with_timestamp(monkeypatch):
    class DummyWrapper:
        def __init__(self, jwk_set):
            self.input = jwk_set

    monkeypatch.setattr(jwk_set_cache_module, 'PyJWTSetWithTimestamp', DummyWrapper)

    cache = JWKSetCache(60)
    mock_jwk_set = object()
    cache.put(mock_jwk_set)

    assert isinstance(cache.jwk_set_with_timestamp, DummyWrapper)
    assert cache.jwk_set_with_timestamp.input is mock_jwk_set

def test_put_none_clears_cache(monkeypatch):
    monkeypatch.setattr(jwk_set_cache_module, 'PyJWTSetWithTimestamp', lambda x: None)

    cache = JWKSetCache(60)
    cache.jwk_set_with_timestamp = object()
    cache.put(None)

    assert cache.jwk_set_with_timestamp is None
