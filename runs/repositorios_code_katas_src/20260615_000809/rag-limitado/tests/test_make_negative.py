import pytest
from repositorios.code_katas.src.return_negative import make_negative

# Teste feliz: números positivos, negativos e floats retornam -abs(n)
@pytest.mark.parametrize("input_value, expected", [
    (0, 0),
    (5, -5),
    (-5, -5),
    (3.14, -3.14),
    (-2.7, -2.7),
])
def test_make_negative_happy_path(input_value, expected):
    assert make_negative(input_value) == expected

# Teste de exceção: entradas não numéricas devem levantar TypeError
@pytest.mark.parametrize("bad_input", [
    "abc",
    (1, 2),
    None
])
def test_make_negative_raises_type_error_for_non_numeric(bad_input):
    with pytest.raises(TypeError):
        make_negative(bad_input)
