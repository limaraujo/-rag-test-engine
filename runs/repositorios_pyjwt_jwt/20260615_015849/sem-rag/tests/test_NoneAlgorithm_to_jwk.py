import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# Verifica que NoneAlgorithm.to_jwk levanta NotImplementedError (caso simples)
def test_to_jwk_raises_not_implemented_happy_path():
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.to_jwk(key_obj=None, as_dict=False)

# Verifica que NoneAlgorithm.to_jwk levanta NotImplementedError ao usar o flag as_dict=True
def test_to_jwk_raises_not_implemented_with_dict_flag():
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.to_jwk(key_obj="some_key", as_dict=True)
