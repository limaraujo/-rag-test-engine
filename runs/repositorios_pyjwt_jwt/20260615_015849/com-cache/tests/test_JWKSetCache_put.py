import typing
import repositorios.pyjwt.jwt.jwk_set_cache as cache_mod
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

def test_put_with_non_none_jwkset_stores_timestamp_wrapper(monkeypatch):
    class DummyWrapper:
        last_jwk_set: typing.Any = None

        def __init__(self, jwk_set):
            type(self).last_jwk_set = jwk_set
            self.jwk_set = jwk_set

    monkeypatch.setattr(cache_mod, "PyJWTSetWithTimestamp", DummyWrapper)
    cache = cache_mod.JWKSetCache(lifespan=60)
    jwk_set = {"kid": "abc"}  # minimal dummy value
    cache.put(jwk_set)

    assert isinstance(cache.jwk_set_with_timestamp, DummyWrapper)
    assert DummyWrapper.last_jwk_set is jwk_set

def test_put_none_clears_cache(monkeypatch):
    class DummyWrapper:
        def __init__(self, jwk_set):
            pass

    monkeypatch.setattr(cache_mod, "PyJWTSetWithTimestamp", DummyWrapper)
    cache = cache_mod.JWKSetCache(lifespan=60)
    cache.put(None)

    assert cache.jwk_set_with_timestamp is None
