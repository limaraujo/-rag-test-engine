import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# curto: verifica que NoneAlgorithm.to_jwk levanta NotImplementedError para diversos key_obj com as_dict=False
@pytest.mark.parametrize("key_obj", [123, "abc", None, {"k": "v"}])
def test_none_algorithm_to_jwk_not_implemented_false(key_obj):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.to_jwk(key_obj, as_dict=False)

# curto: verifica que NoneAlgorithm.to_jwk levanta NotImplementedError para diversos key_obj com as_dict=True
@pytest.mark.parametrize("key_obj", [123, "abc", None, {"k": "v"}])
def test_none_algorithm_to_jwk_not_implemented_true(key_obj):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.to_jwk(key_obj, as_dict=True)
