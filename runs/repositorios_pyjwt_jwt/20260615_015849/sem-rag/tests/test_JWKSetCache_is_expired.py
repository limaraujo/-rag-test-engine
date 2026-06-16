import time
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache



class DummyTimestamp:
    def __init__(self, ts):
        self._ts = ts

    def get_timestamp(self):
        return self._ts


def _make_cache(ts, lifespan):
    c = object.__new__(JWKSetCache)
    c.jwk_set_with_timestamp = DummyTimestamp(ts)
    c.lifespan = lifespan
    return c


# Test: happy path - expired when current monotonic exceeds timestamp + lifespan
def test_is_expired_true_when_time_passes(monkeypatch):
    ts = 5
    lifespan = 10
    cache = _make_cache(ts, lifespan)
    monkeypatch.setattr(time, "monotonic", lambda: ts + lifespan + 1)
    assert cache.is_expired() is True


# Test: not expired when current monotonic has not yet reached expiry
def test_is_expired_false_before_expiry(monkeypatch):
    ts = 5
    lifespan = 10
    cache = _make_cache(ts, lifespan)
    monkeypatch.setattr(time, "monotonic", lambda: ts + lifespan - 1)
    assert cache.is_expired() is False


# Test: not expired when timestamp is missing (None)
def test_is_expired_false_when_timestamp_missing():
    cache = object.__new__(JWKSetCache)
    cache.jwk_set_with_timestamp = None
    cache.lifespan = 10
    assert cache.is_expired() is False


# Test: not expired when lifespan is non-positive
def test_is_expired_false_when_non_positive_lifespan(monkeypatch):
    ts = 5
    cache = _make_cache(ts, -1)
    monkeypatch.setattr(time, "monotonic", lambda: ts + 100)
    assert cache.is_expired() is False
