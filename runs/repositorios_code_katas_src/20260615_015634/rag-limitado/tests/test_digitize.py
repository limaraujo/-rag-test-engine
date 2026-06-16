import pytest
from repositorios.code_katas.src.convert import digitize

# verifica o caminho feliz com múltiplos casos (zero, número de várias casas, e com zeros internos)
@pytest.mark.parametrize("input_value,expected", [
    (0, [0]),
    (12345, [5, 4, 3, 2, 1]),
    (8070, [0, 7, 0, 8]),
])
def test_digitize_happy_path_multiple_inputs(input_value, expected):
    assert digitize(input_value) == expected

# verifica exceção para inteiros negativos (valor não suportado pela função)
def test_digitize_negative_raises_value_error():
    with pytest.raises(ValueError):
        digitize(-123)

# verifica exceção com entrada não numérica
def test_digitize_non_digit_string_raises_value_error():
    with pytest.raises(ValueError):
        digitize("abc")
