import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

def _make_jwk(jwk_data: dict) -> PyJWK:
    obj = PyJWK.__new__(PyJWK)
    obj._jwk_data = jwk_data
    return obj

def _get_public_key_use(jwk: PyJWK):
    value = jwk.public_key_use
    if callable(value):
        return value()
    return value

def test_public_key_use_happy_path():
    jwk = _make_jwk({"use": "sig"})
    assert _get_public_key_use(jwk) == "sig"

def test_public_key_use_missing_key_returns_none():
    jwk = _make_jwk({"kid": "abc123"})
    assert _get_public_key_use(jwk) is None

def test_public_key_use_value_none_returns_none():
    jwk = _make_jwk({"use": None})
    assert _get_public_key_use(jwk) is None

def test_public_key_use_ignores_other_keys():
    jwk = _make_jwk({"kid": "abc", "use": "enc", "alg": "RS256"})
    assert _get_public_key_use(jwk) == "enc"
