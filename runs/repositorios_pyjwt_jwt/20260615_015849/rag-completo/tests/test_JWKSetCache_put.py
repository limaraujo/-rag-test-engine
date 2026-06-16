from unittest.mock import patch
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

def test_put_sets_cache_when_jwk_set_provided():
    with patch("repositorios.pyjwt.jwt.jwk_set_cache.PyJWTSetWithTimestamp") as MockWrapper:
        MockWrapper.return_value = "wrapped"
        cache = JWKSetCache(60)
        dummy_jwk_set = object()
        cache.put(dummy_jwk_set)
        MockWrapper.assert_called_once_with(dummy_jwk_set)
        assert cache.jwk_set_with_timestamp == "wrapped"

def test_put_clears_cache_when_none():
    with patch("repositorios.pyjwt.jwt.jwk_set_cache.PyJWTSetWithTimestamp") as MockWrapper:
        cache = JWKSetCache(60)
        cache.put(None)
        MockWrapper.assert_not_called()
        assert cache.jwk_set_with_timestamp is None
