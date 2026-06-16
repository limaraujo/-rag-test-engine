import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm


# Verifica que from_jwk levanta NotImplementedError para entradas de string ou JWKDict
@pytest.mark.parametrize("jwk_input", [
    "dummy_jwk",
    {"kty": "RSA"}
])
def test_from_jwk_raises_not_implemented_for_various_inputs(jwk_input):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.from_jwk(jwk_input)
