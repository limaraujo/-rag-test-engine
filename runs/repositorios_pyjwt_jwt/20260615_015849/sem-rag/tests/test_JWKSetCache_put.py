import repositorios.pyjwt.jwt.jwk_set_cache as jwk_set_cache_module
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

def test_put_non_none_calls_pyjwtset_with_timestamp(monkeypatch):
    class DummyPyJWTSetWithTimestamp:
        def __init__(self, jwk_set):
            self.jwk_set = jwk_set

    monkeypatch.setattr(
        jwk_set_cache_module, "PyJWTSetWithTimestamp", DummyPyJWTSetWithTimestamp, raising=True
    )

    cache = jwk_set_cache_module.JWKSetCache(lifespan=3600)
    sample_jwk_set = object()
    cache.put(sample_jwk_set)

    assert isinstance(cache.jwk_set_with_timestamp, DummyPyJWTSetWithTimestamp)
    assert cache.jwk_set_with_timestamp.jwk_set is sample_jwk_set

def test_put_none_clears_cache(monkeypatch):
    class DummyPyJWTSetWithTimestamp:
        def __init__(self, jwk_set):
            self.jwk_set = jwk_set

    monkeypatch.setattr(
        jwk_set_cache_module, "PyJWTSetWithTimestamp", DummyPyJWTSetWithTimestamp, raising=True
    )

    cache = jwk_set_cache_module.JWKSetCache(lifespan=3600)
    cache.put(object())  # pre-populate to ensure non-None state
    assert cache.jwk_set_with_timestamp is not None

    cache.put(None)
    assert cache.jwk_set_with_timestamp is None
