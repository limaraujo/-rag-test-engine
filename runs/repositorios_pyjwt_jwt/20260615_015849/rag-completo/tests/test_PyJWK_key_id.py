import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

# Verifica o caminho feliz (kid presente) e caso de borda (kid ausente) via parametrização
@pytest.mark.parametrize("jwk_data, expected", [
    ({"kid": "my-key-id"}, "my-key-id"),
    ({}, None),
])
def test_key_id_returns_kid_or_none(jwk_data, expected):
    obj = PyJWK.__new__(PyJWK)
    obj._jwk_data = jwk_data
    key_id_member = obj.key_id
    actual = key_id_member() if callable(key_id_member) else key_id_member
    assert actual == expected
