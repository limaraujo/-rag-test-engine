import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# verifica que NoneAlgorithm.to_jwk levanta NotImplementedError para diversos key_obj
@pytest.mark.parametrize("key_obj", [None, 0, "str", object()])
def test_to_jwk_raises_not_implemented_for_various_keys(key_obj):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.to_jwk(key_obj)

# verifica que as_dict True/False não afeta o comportamento (lança NotImplementedError)
@pytest.mark.parametrize("as_dict", [False, True])
def test_to_jwk_raises_not_implemented_with_as_dict_flag(as_dict):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.to_jwk(key_obj=object(), as_dict=as_dict)
