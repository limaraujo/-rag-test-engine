import pytest
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# short
@pytest.mark.parametrize("kwargs", [
    {},
    {"curve": "SECP256R1"},
    {"custom": 42},
    {"nested": {"a": 1, "b": [2, 3]}},
])
def test_okp_algorithm_init_accepts_various_kwargs(kwargs):
    # happy path: __init__ should accept arbitrary kwargs and initialize without error
    obj = OKPAlgorithm(**kwargs)
    assert isinstance(obj, OKPAlgorithm)
