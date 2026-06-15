import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

def _make_jwk(jwk_data):
    obj = PyJWK.__new__(PyJWK)
    obj._jwk_data = jwk_data
    return obj

def _resolve_key_id(jwk):
    kid = getattr(jwk, "key_id")
    if callable(kid):
        return kid()
    return kid

@pytest.mark.parametrize("jwk_data, expected", [
    ({"kid": "abc123"}, "abc123"),
    ({}, None),
    ({"kid": None}, None),
])
def test_key_id_values(jwk_data, expected):
    jwk = _make_jwk(jwk_data)
    assert _resolve_key_id(jwk) == expected
