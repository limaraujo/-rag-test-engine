import pytest
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm


# Verifica o caminho feliz: OKPAlgorithm.__init__ aceita vários kwargs sem falhar e retorna a instância
@pytest.mark.parametrize("kwargs", [
    {},
    {"foo": "bar"},
    {"key1": 123, "key2": None},
    {"a": True, "b": [1, 2, 3]},
])
def test_okp_algorithm_init_accepts_various_kwargs(kwargs):
    obj = OKPAlgorithm(**kwargs)
    assert isinstance(obj, OKPAlgorithm)

# Verifica que __init__ não atribui atributos com base nos kwargs (sem efeitos colaterais)
@pytest.mark.parametrize("kwargs", [
    {},
    {"foo": "bar"},
    {"x": 1, "y": 2},
])
def test_okp_algorithm_init_does_not_set_kwargs_as_attributes(kwargs):
    obj = OKPAlgorithm(**kwargs)
    for key in kwargs.keys():
        assert not hasattr(obj, key)
