import time
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

class _StubTimestamp:
    def __init__(self, ts: int) -> None:
        self._ts = ts
    def get_timestamp(self) -> int:
        return self._ts

# Test 1: happy path - pode expirar quando tempo atual > timestamp + lifespan
# Verifica que is_expired retorna True no cenário de expiração
def test_is_expired_happy_path(monkeypatch):
    inst = JWKSetCache.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = _StubTimestamp(100)
    inst.lifespan = 5
    monkeypatch.setattr(time, "monotonic", lambda: 106)
    assert inst.is_expired() is True

# Test 2: não expira quando jwk_set_with_timestamp é None
# Verifica que is_expired retorna False se não houver timestamp associado
def test_is_expired_none_jwkset(monkeypatch):
    inst = JWKSetCache.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = None
    inst.lifespan = 10
    monkeypatch.setattr(time, "monotonic", lambda: 123)
    assert inst.is_expired() is False

# Test 3: não expira quando lifespan é negativo
# Verifica que is_expired retorna False se lifespan <= -1
def test_is_expired_negative_lifespan(monkeypatch):
    inst = JWKSetCache.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = _StubTimestamp(0)
    inst.lifespan = -1
    monkeypatch.setattr(time, "monotonic", lambda: 10)
    assert inst.is_expired() is False

# Test 4: não expira ainda quando tempo atual <= timestamp + lifespan
# Verifica a parte de branch "não expirou ainda"
def test_is_expired_not_yet_expired(monkeypatch):
    inst = JWKSetCache.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = _StubTimestamp(50)
    inst.lifespan = 20
    monkeypatch.setattr(time, "monotonic", lambda: 69)
    assert inst.is_expired() is False
