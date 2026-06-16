import pytest
from repositorios.code_katas.src.convert import digitize

# curto: happy path - converte inteiros simples para lista invertida de dígitos
@pytest.mark.parametrize("input_value, expected", [
    (0, [0]),
    (123, [3, 2, 1]),
    (90, [0, 9]),
    (5, [5]),
])
def test_digitize_happy_path(input_value, expected):
    assert digitize(input_value) == expected

# curto: exceção listada - entrada negativa levanta ValueError
def test_digitize_negative_raises():
    with pytest.raises(ValueError):
        digitize(-123)

# curto: exceção listada - entrada não-integer (float) levanta ValueError
def test_digitize_float_raises():
    with pytest.raises(ValueError):
        digitize(12.3)
