import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# verifica que NotImplementedError é levantada para entradas JWK em formatos string e dict
@pytest.mark.parametrize("jwk_input", [
    "{}",  # string input
    {"kty": "oct", "k": "dummy"}  # dict input
])
def test_none_algorithm_from_jwk_raises_not_implemented(jwk_input):
    # exceção NotImplementedError para qualquer input de jwk
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.from_jwk(jwk_input)
