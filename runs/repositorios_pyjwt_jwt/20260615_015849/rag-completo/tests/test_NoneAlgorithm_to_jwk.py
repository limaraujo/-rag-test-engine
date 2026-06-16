import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm



# curto: verifica NotImplementedError ao chamar NoneAlgorithm.to_jwk por meio da classe
@pytest.mark.parametrize("key_obj", [None, {}, 123, "algo"])
@pytest.mark.parametrize("as_dict", [False, True])
def test_to_jwk_class_raises_not_implemented(key_obj, as_dict):
    with pytest.raises(NotImplementedError):
        NoneAlgorithm.to_jwk(key_obj, as_dict)


# curto: verifica NotImplementedError ao criar uma instância e chamar to_jwk
@pytest.mark.parametrize("key_obj", [None, {}, 123, "algo"])
@pytest.mark.parametrize("as_dict", [False, True])
def test_to_jwk_instance_raises_not_implemented(key_obj, as_dict):
    inst = NoneAlgorithm()
    with pytest.raises(NotImplementedError):
        inst.to_jwk(key_obj, as_dict)
