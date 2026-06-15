import time
import pytest
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

# helper to simulate a timestamp provider
class _TimestampProvider:
    def __init__(self, ts: float):
        self._ts = ts

    def get_timestamp(self) -> float:
        return self._ts

# Test: não expira quando jwk_set_with_timestamp é None (caso de não expiração)
def test_is_expired_without_timestamp_false():
    obj = JWKSetCache.__new__(JWKSetCache)
    obj.jwk_set_with_timestamp = None
    obj.lifespan = 60
    assert obj.is_expired() is False

# Test: não expira quando lifespan <= -1 (limite negativo)
def test_is_expired_with_negative_lifespan_false():
    ts = time.monotonic()
    obj = JWKSetCache.__new__(JWKSetCache)
    obj.jwk_set_with_timestamp = _TimestampProvider(ts)
    obj.lifespan = -1
    assert obj.is_expired() is False

# Test: não expira quando ainda está dentro do lifespan (caso feliz de não expiração)
def test_is_expired_false_when_within_lifespan():
    ts = time.monotonic() - 1.0  # timestamp recente
    obj = JWKSetCache.__new__(JWKSetCache)
    obj.jwk_set_with_timestamp = _TimestampProvider(ts)
    obj.lifespan = 5.0  # small lifespan
    assert obj.is_expired() is False

# Test: expira quando o timestamp é suficientemente antigo (past lifespan)
def test_is_expired_true_when_past_lifespan():
    ts = time.monotonic() - 1000.0  # timestamp bem antigo
    obj = JWKSetCache.__new__(JWKSetCache)
    obj.jwk_set_with_timestamp = _TimestampProvider(ts)
    obj.lifespan = 60.0
    assert obj.is_expired() is True
