import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ImmatureSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

def _make_instance():
    return PyJWT.__new__(PyJWT)

def test_validate_nbf_happy_path_no_exception():
    instance = _make_instance()
    payload = {"nbf": "1000"}
    now = 1000
    leeway = 0
    instance._validate_nbf(payload, now, leeway)

def test_validate_nbf_raises_decode_error_on_non_int():
    instance = _make_instance()
    payload = {"nbf": "not-a-number"}
    with pytest.raises(DecodeError):
        instance._validate_nbf(payload, 0, 0)

def test_validate_nbf_raises_immature_signature_when_nbf_is_future():
    instance = _make_instance()
    now = 1000
    leeway = 0
    payload = {"nbf": str(now + leeway + 1)}
    with pytest.raises(ImmatureSignatureError):
        instance._validate_nbf(payload, now, leeway)

def test_validate_nbf_missing_nbf_key_raises_key_error():
    instance = _make_instance()
    payload = {}
    with pytest.raises(KeyError):
        instance._validate_nbf(payload, 0, 0)
