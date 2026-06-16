import json
import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

# happy path: valid JSON loads and from_dict is invoked with parsed dict and algorithm
@pytest.mark.parametrize("algorithm", [None, "RS256"])
def test_from_json_happy_path(monkeypatch, algorithm):
    captured = {}

    def fake_from_dict(cls, obj, alg=None):
        captured['cls'] = cls
        captured['obj'] = obj
        captured['alg'] = alg
        return "FAKE_JWK"

    monkeypatch.setattr(PyJWK, "from_dict", classmethod(fake_from_dict), raising=True)

    json_str = '{"kty": "RSA", "kid": "abc"}'
    result = PyJWK.from_json(json_str, algorithm)

    assert result == "FAKE_JWK"
    assert captured['cls'] is PyJWK
    assert captured['obj'] == {"kty": "RSA", "kid": "abc"}
    if algorithm is not None:
        assert captured['alg'] == algorithm
    else:
        assert captured['alg'] is None

# error path: invalid JSON should raise JSONDecodeError
def test_from_json_invalid_json_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        PyJWK.from_json("not json", None)
