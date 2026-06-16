import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# teste happy path: decode delega para decode_complete e retorna o payload
def test_decode_happy_path_calls_decode_complete_and_returns_payload(monkeypatch):
    instance = PyJWS()
    captured = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, detached_payload=None, **kwargs):
        captured['args'] = (jwt, key, algorithms, options, detached_payload, kwargs)
        return {'payload': 'payload_value'}

    monkeypatch.setattr(PyJWS, "decode_complete", fake_decode_complete, raising=True)

    result = instance.decode("header.payload", key="mykey", algorithms=None, options=None, detached_payload=None)

    assert result == 'payload_value'
    assert captured['args'][0] == "header.payload"
    assert captured['args'][1] == "mykey"
    assert captured['args'][2] is None
    assert captured['args'][3] is None
    assert captured['args'][4] is None
    assert captured['args'][5] == {}

# teste kwargs extra: warning deprectation é emitida e o resultado ainda é propagado
def test_decode_with_extra_kwargs_emits_warning_and_propagates_result(monkeypatch):
    instance = PyJWS()
    captured = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, detached_payload=None, **kwargs):
        captured['args'] = (jwt, key, algorithms, options, detached_payload, kwargs)
        return {'payload': 'payload_with_warning'}

    monkeypatch.setattr(PyJWS, "decode_complete", fake_decode_complete, raising=True)

    with pytest.warns(Warning):
        result = instance.decode("jwt", key="k", extra="x")

    assert result == 'payload_with_warning'
    # Observa-se que kwargs não são repassados para decode_complete, resultando em {}
    assert captured['args'][5] == {}

# teste detached_payload é repassado para decode_complete
def test_decode_passes_detached_payload_correctly(monkeypatch):
    instance = PyJWS()
    captured = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, detached_payload=None, **kwargs):
        captured['args'] = (jwt, key, algorithms, options, detached_payload)
        return {'payload': 'ok'}

    monkeypatch.setattr(PyJWS, "decode_complete", fake_decode_complete, raising=True)

    result = instance.decode("jwt", detached_payload=b"detached")

    assert result == 'ok'
    assert captured['args'][4] == b"detached"
