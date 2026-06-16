import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK


@pytest.mark.parametrize("jwk_data, expected", [
    ({"use": "sig"}, "sig"),
    ({}, None),
    ({"use": None}, None),
])
def test_public_key_use(jwk_data, expected):
    obj = object.__new__(PyJWK)
    obj._jwk_data = jwk_data
    pub = obj.public_key_use
    result = pub() if callable(pub) else pub
    assert result == expected
