import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm


# verifica que NoneAlgorithm.from_jwk levanta NotImplementedError para jwk de string e de dict
@pytest.mark.parametrize("jwk", [
    "dummy-string-jwk",
    {"kty": "oct", "k": "deadbeef"},
])
def test_from_jwk_raises_not_implemented(jwk):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.from_jwk(jwk)
