from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# happy path: verify jwk_set is stored and timestamp uses time.monotonic
def test_init_happy_path_stores_jwk_set_and_timestamp(monkeypatch):
    class DummyJWKSet:
        pass
    jwk = DummyJWKSet()
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jwk.time.monotonic", lambda: 123.456)
    instance = PyJWTSetWithTimestamp(jwk)
    assert instance.jwk_set is jwk
    assert instance.timestamp == 123.456
    assert isinstance(instance.timestamp, float)

# edge case: input object is not mutated by __init__
def test_init_does_not_mutate_input_object(monkeypatch):
    class DummyJWKSet:
        pass
    jwk = DummyJWKSet()
    jwk.marker = "unchanged"
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jwk.time.monotonic", lambda: 0.0)
    PyJWTSetWithTimestamp(jwk)
    assert getattr(jwk, "marker") == "unchanged"
