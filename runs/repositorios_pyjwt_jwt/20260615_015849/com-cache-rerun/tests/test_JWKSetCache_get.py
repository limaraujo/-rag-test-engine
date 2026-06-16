from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

class DummyJWKSetWithTimestamp:
    def __init__(self, value):
        self._value = value
    def get_jwk_set(self):
        return self._value

# curto: caminho verdadeiro quando jwk_set_with_timestamp é None
def test_get_returns_none_when_jwk_set_with_timestamp_is_none():
    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = None
    inst.is_expired = lambda: False  # não utilizado neste cenário
    assert inst.get() is None

# curto: caminho falso (não expirado) retorna o conjunto JWK
def test_get_returns_jwk_set_when_not_expired():
    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = DummyJWKSetWithTimestamp("expected_jwk_set")
    inst.is_expired = lambda: False
    assert inst.get() == "expected_jwk_set"

# curto: caminho verdadeiro devido à expiração (is_expired retorna True) -> None
def test_get_returns_none_when_expired():
    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = DummyJWKSetWithTimestamp("ignored_jwk_set")
    inst.is_expired = lambda: True
    assert inst.get() is None
