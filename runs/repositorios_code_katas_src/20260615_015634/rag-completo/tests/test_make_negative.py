import pytest
from repositorios.code_katas.src.return_negative import make_negative

# Verifica retornos corretos para números positivos, negativos e zero (caminho feliz)
@pytest.mark.parametrize("input_number, expected", [(3, -3), (-7, -7), (0, 0)])
def test_make_negative_happy_path(input_number, expected):
    assert make_negative(input_number) == expected

# Verifica que passar um input inválido levanta TypeError (exceção relevante)
def test_make_negative_type_error_on_string():
    with pytest.raises(TypeError):
        make_negative("abc")
