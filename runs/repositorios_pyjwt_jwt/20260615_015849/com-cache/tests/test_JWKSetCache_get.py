from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

def _make_cache(jwk_set_with_timestamp=None, is_expired_func=None):
    obj = object.__new__(JWKSetCache)
    obj.jwk_set_with_timestamp = jwk_set_with_timestamp
    obj.is_expired = is_expired_func if is_expired_func is not None else (lambda: False)
    return obj

# verifica que retorna None quando jwk_set_with_timestamp é None (caso de borda)
def test_get_none_when_jwk_set_missing():
    cache = _make_cache(jwk_set_with_timestamp=None, is_expired_func=lambda: False)
    assert cache.get() is None

# verifica que retorna None quando a checagem de expiração indica expirado (branch de erro)
def test_get_none_when_expired():
    class DummyJWKS:
        def get_jwk_set(self):
            return "should_not_be_called"
    cache = _make_cache(jwk_set_with_timestamp=DummyJWKS(), is_expired_func=lambda: True)
    assert cache.get() is None

# verifica que retorna o JWKSet quando não expirado (happy path)
def test_get_returns_jwk_set_when_not_expired():
    class DummyJWKS:
        def __init__(self, value):
            self._value = value
        def get_jwk_set(self):
            return self._value
    expected = "jwkset"
    cache = _make_cache(jwk_set_with_timestamp=DummyJWKS(expected), is_expired_func=lambda: False)
    assert cache.get() == expected
