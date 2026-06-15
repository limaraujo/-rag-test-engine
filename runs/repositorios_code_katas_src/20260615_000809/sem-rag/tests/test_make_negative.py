import pytest
from repositorios.code_katas.src.return_negative import make_negative

# Verifica happy path: números positivos e zero retornam negativo do valor absoluto
@pytest.mark.parametrize("input_value, expected", [
    (1, -1),
    (2.5, -2.5),
    (0, 0),
])
def test_make_negative_positive_and_zero(input_value, expected):
    assert make_negative(input_value) == expected

# Verifica casos com números negativos: retorna o próprio valor (negativo) já que o valor absoluto é o próprio valor
@pytest.mark.parametrize("input_value, expected", [
    (-1, -1),
    (-3.7, -3.7),
    (-2.0, -2.0),
])
def test_make_negative_negative_numbers(input_value, expected):
    assert make_negative(input_value) == expected
