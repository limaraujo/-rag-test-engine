import pytest
from repositorios.code_katas.src.return_negative import make_negative

# Verifica retorno negativo da magnitude para vários inputs: positivo, negativo, zero e float
@pytest.mark.parametrize("input_value, expected", [
    (5, -5),
    (-3, -3),
    (0, 0),
    (2.5, -2.5),
])
def test_make_negative_various_inputs(input_value, expected):
    assert make_negative(input_value) == expected
