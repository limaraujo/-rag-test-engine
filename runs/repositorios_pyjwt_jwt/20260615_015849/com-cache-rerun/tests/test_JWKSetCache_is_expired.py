import time
import pytest
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache


class DummyWithTimestamp:
    def __init__(self, ts: int):
        self._ts = ts

    def get_timestamp(self) -> int:
        return self._ts

def _make_instance(jwk_ts: DummyWithTimestamp | None, lifespan: int) -> JWKSetCache:
    obj = object.__new__(JWKSetCache)
    obj.jwk_set_with_timestamp = jwk_ts
    obj.lifespan = lifespan
    return obj

# short: happy path - is_expired should be True when time has surpassed timestamp + lifespan
def test_is_expired_happy_path(monkeypatch):
    jwk = DummyWithTimestamp(100)
    inst = _make_instance(jwk, lifespan=5)
    monkeypatch.setattr(time, "monotonic", lambda: 106)
    assert inst.is_expired() is True

# short: branch where current time is not past timestamp + lifespan -> False
def test_is_expired_not_expired_due_to_time(monkeypatch):
    jwk = DummyWithTimestamp(100)
    inst = _make_instance(jwk, lifespan=5)
    monkeypatch.setattr(time, "monotonic", lambda: 104)
    assert inst.is_expired() is False

# short: edge case where jwk_set_with_timestamp is None -> False
def test_is_expired_none_jwk_set(monkeypatch):
    inst = _make_instance(None, lifespan=5)
    monkeypatch.setattr(time, "monotonic", lambda: 200)
    assert inst.is_expired() is False

# short: edge case where lifespan <= -1 -> False
def test_is_expired_invalid_lifespan(monkeypatch):
    jwk = DummyWithTimestamp(100)
    inst = _make_instance(jwk, lifespan=-1)
    monkeypatch.setattr(time, "monotonic", lambda: 200)
    assert inst.is_expired() is False
