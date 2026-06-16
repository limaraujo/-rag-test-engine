import json
import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

# happy path: JSON válido é parseado e delega para from_dict, retornando o valor de from_dict
@pytest.mark.parametrize("input_json, expected_dict", [
    ('{"a":1}', {"a":1}),
    ('{"b":"x","c":true}', {"b":"x","c": True}),
])
def test_from_json_happy_path_calls_from_dict_and_returns_value(input_json, expected_dict, monkeypatch):
    calls = {}
    def fake_from_dict(*args, **kwargs):
        if len(args) == 1:
            parsed = args[0]
        elif len(args) >= 2:
            parsed = args[1]
        else:
            parsed = None
        calls['arg'] = parsed
        return "SENTINEL"
    monkeypatch.setattr(PyJWKSet, "from_dict", fake_from_dict)
    result = PyJWKSet.from_json(input_json)
    assert result == "SENTINEL"
    assert calls['arg'] == expected_dict

# error path: invalid JSON raises JSONDecodeError e json não é decodificado
def test_from_json_invalid_json_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        PyJWKSet.from_json("not json")
