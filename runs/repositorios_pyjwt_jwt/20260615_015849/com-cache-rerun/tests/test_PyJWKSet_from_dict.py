import pytest
from repositorios.pyjwt.jwt.exceptions import PyJWKSetError
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

def test_from_dict_happy_path():
    input_dict = {"keys": [{"kty": "oct", "kid": "1", "k": "AQID"}]}
    result = PyJWKSet.from_dict(input_dict)
    assert isinstance(result, PyJWKSet)
    assert isinstance(result.keys, list)
    assert len(result.keys) == len(input_dict["keys"])

def test_from_dict_defaults_to_empty_when_keys_missing():
    input_dict = {}
    with pytest.raises(PyJWKSetError):
        PyJWKSet.from_dict(input_dict)
