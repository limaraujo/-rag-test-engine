from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

# Verifica retorna None quando não há jwk_set (jwk_set_with_timestamp é None)
def test_get_returns_none_when_no_jwk_set():
    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = None
    inst.is_expired = lambda: False
    assert inst.get() is None

# Verifica retorna o PyJWKSet quando não está expirado
def test_get_returns_jwkset_when_not_expired():
    class DummyWithTimestamp:
        def __init__(self, value):
            self._value = value
        def get_jwk_set(self):
            return self._value

    value = object()
    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = DummyWithTimestamp(value)
    inst.is_expired = lambda: False
    result = inst.get()
    assert result is value
