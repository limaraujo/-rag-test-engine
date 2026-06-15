import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# Testa: exceção NotImplementedError para diferentes tipos de jwk (string e JWKDict)
@pytest.mark.parametrize("jwk", [
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",  # fotocopia de uma string JWK simulada
    {"kty": "EC", "crv": "P-256", "x": "A", "y": "B"}  # simulando um JWK_dict
])
def test_none_algorithm_from_jwk_raises_not_implemented(jwk):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.from_jwk(jwk)
