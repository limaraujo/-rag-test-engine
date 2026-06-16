import pytest
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# happy path: instancia OKPAlgorithm sem kwargs sem levantar exceção
def test_okp_algorithm_init_no_kwargs():
    obj = OKPAlgorithm()
    assert isinstance(obj, OKPAlgorithm)

# accepts arbitrary kwargs: garante que __init__ aceita kwargs não mapeados sem erro
@pytest.mark.parametrize("init_kwargs", [
    {},
    {"foo": "bar"},
    {"a": 1, "b": None, "c": [1, 2, 3]}
])
def test_okp_algorithm_init_accepts_kwargs(init_kwargs):
    obj = OKPAlgorithm(**init_kwargs)
    assert isinstance(obj, OKPAlgorithm)
