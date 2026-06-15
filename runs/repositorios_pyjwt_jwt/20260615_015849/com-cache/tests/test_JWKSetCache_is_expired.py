import time
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache



class DummyJWKSetWithTimestamp:
    def __init__(self, ts):
        self._ts = ts

    def get_timestamp(self):
        return self._ts


# test: happy path - is_expired should be True when current time > timestamp + lifespan
def test_is_expired_happy_path(monkeypatch):
    # cenário: jwk_set_with_timestamp presente, lifespan > -1, tempo atual já passou do limite
    ts = 100
    lifespan = 10
    monotonic_value = 111
    monkeypatch.setattr(time, "monotonic", lambda: monotonic_value)

    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = DummyJWKSetWithTimestamp(ts)
    inst.lifespan = lifespan

    assert inst.is_expired() is True


# test: not expired - current time not yet past the expiry threshold
def test_is_expired_not_expired(monkeypatch):
    # cenário: jwk_set_with_timestamp presente, lifespan > -1, tempo atual ainda não atingiu expiry
    ts = 100
    lifespan = 10
    monotonic_value = 110
    monkeypatch.setattr(time, "monotonic", lambda: monotonic_value)

    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = DummyJWKSetWithTimestamp(ts)
    inst.lifespan = lifespan

    assert inst.is_expired() is False


# test: no jwk set timestamp - should be False regardless of time
def test_is_expired_none_jwk_set(monkeypatch):
    # cenário: jwk_set_with_timestamp é None -> não expira
    ts = 100  # não utilizado
    lifespan = 10
    monotonic_value = 1000
    monkeypatch.setattr(time, "monotonic", lambda: monotonic_value)

    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = None
    inst.lifespan = lifespan

    assert inst.is_expired() is False


# test: invalid lifespan (<= -1) - should be False
def test_is_expired_invalid_lifespan(monkeypatch):
    # cenário: lifespan <= -1 impede expiração
    ts = 100
    lifespan = -1
    monotonic_value = 1000
    monkeypatch.setattr(time, "monotonic", lambda: monotonic_value)

    inst = object.__new__(JWKSetCache)
    inst.jwk_set_with_timestamp = DummyJWKSetWithTimestamp(ts)
    inst.lifespan = lifespan

    assert inst.is_expired() is False
