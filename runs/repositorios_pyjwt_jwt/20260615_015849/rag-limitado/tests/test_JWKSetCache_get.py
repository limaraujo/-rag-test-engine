from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

class DummyContainer:
    def __init__(self, value):
        self._value = value
    def get_jwk_set(self):
        return self._value

# Verifica: retorna None quando jwk_set_with_timestamp é None
def test_get_returns_none_when_missing_jwk_set():
    cache = object.__new__(JWKSetCache)
    cache.jwk_set_with_timestamp = None
    cache.is_expired = lambda: False
    assert cache.get() is None

# Verifica: retorna None quando o cache está expirado
def test_get_returns_none_when_expired():
    cache = object.__new__(JWKSetCache)
    cache.jwk_set_with_timestamp = DummyContainer("SENTINEL")
    cache.is_expired = lambda: True
    assert cache.get() is None

# Verifica: retorna o JWK set válido quando não expirado
def test_get_returns_jwk_set_when_valid():
    cache = object.__new__(JWKSetCache)
    expected = "SENTINEL"
    cache.jwk_set_with_timestamp = DummyContainer(expected)
    cache.is_expired = lambda: False
    assert cache.get() == expected
