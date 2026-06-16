import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

# Verifica o retorno do campo 'use' em cenários: presente, ausente e None
@pytest.mark.parametrize("jwk_data,expected", [
    ({"use": "sig"}, "sig"),
    ({}, None),
    ({"use": None}, None),
])
def test_public_key_use(jwk_data, expected):
    jwk = object.__new__(PyJWK)
    jwk._jwk_data = jwk_data
    pub_attr = getattr(jwk, "public_key_use")
    result = pub_attr() if callable(pub_attr) else pub_attr
    assert result == expected
