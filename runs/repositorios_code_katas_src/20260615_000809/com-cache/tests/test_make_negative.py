import pytest
from repositorios.code_katas.src.return_negative import make_negative

# Caminho principal (happy path): números positivos, negativos e zero
@pytest.mark.parametrize("input_number, expected", [
    (5, -5),
    (-5, -5),
    (0, 0),
    (3.7, -3.7),
    (-3.7, -3.7),
])
def test_make_negative_happy_path(input_number, expected):
    assert make_negative(input_number) == expected

# Exceção: entradas não numéricas devem levantar TypeError
@pytest.mark.parametrize("bad_input", ["abc", None])
def test_make_negative_raises_type_error(bad_input):
    with pytest.raises(TypeError):
        make_negative(bad_input)
