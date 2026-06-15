import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# Verifica que NoneAlgorithm.from_jwk levanta NotImplementedError (caso padrão)
def test_none_algorithm_from_jwk_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.from_jwk("")
