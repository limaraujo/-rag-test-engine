import json
import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK


# happy path: parse JSON and forward to from_dict with provided algorithm, return value is propagated
def test_from_json_happy_path_calls_from_dict_and_returns_value(monkeypatch):
    data = '{"kty": "oct", "k": "abc"}'
    captured = {}

    def fake_from_dict(obj, alg):
        captured['obj'] = obj
        captured['alg'] = alg
        return {"result": "ok"}

    monkeypatch.setattr(PyJWK, "from_dict", fake_from_dict)
    result = PyJWK.from_json(data, algorithm="RS256")

    assert result == {"result": "ok"}
    assert captured['obj'] == {"kty": "oct", "k": "abc"}
    assert captured['alg'] == "RS256"

# default None: when algorithm is not provided, None is passed to from_dict
def test_from_json_default_none_passed_through(monkeypatch):
    data = '{"a":1}'
    captured = {}

    def fake_from_dict(obj, alg):
        captured['alg'] = alg
        return "OK"

    monkeypatch.setattr(PyJWK, "from_dict", fake_from_dict)
    result = PyJWK.from_json(data)

    assert result == "OK"
    assert captured['alg'] is None

# invalid JSON should raise JSONDecodeError
def test_from_json_invalid_json_raises():
    data = "not json"
    with pytest.raises(json.JSONDecodeError):
        PyJWK.from_json(data)
