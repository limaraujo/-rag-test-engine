import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

def _make_jwk_with_data(data):
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = data
    return jwk

def test_key_type_returns_value_when_kty_present():
    jwk = _make_jwk_with_data({"kty": "RSA"})
    ktype = jwk.key_type
    if callable(ktype):
        ktype = ktype()
    assert ktype == "RSA"

def test_key_type_returns_none_when_kty_missing():
    jwk = _make_jwk_with_data({})
    ktype = jwk.key_type
    if callable(ktype):
        ktype = ktype()
    assert ktype is None
