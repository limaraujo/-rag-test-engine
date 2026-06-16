import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# Verifica que NoneAlgorithm.to_jwk ainda não é implementado; cobre cenários com as_dict False/True e chamadas estáticas/instância
@pytest.mark.parametrize("as_dict", [False, True])
def test_nonealgorithm_to_jwk_raises_not_implemented(as_dict):
    key = {"k": "v"}  # placeholder de entrada
    try:
        NoneAlgorithm.to_jwk(key_obj=key, as_dict=as_dict)
    except NotImplementedError:
        return
    except TypeError:
        instance = NoneAlgorithm()
        with pytest.raises(NotImplementedError):
            instance.to_jwk(key_obj=key, as_dict=as_dict)
        return
    else:
        assert False, "to_jwk did not raise NotImplementedError as expected"
