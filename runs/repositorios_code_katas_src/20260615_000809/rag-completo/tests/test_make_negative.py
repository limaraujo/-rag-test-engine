import pytest
from repositorios.code_katas.src.return_negative import make_negative


# curto: happy path - cobre números positivos, negativos e zero
@pytest.mark.parametrize("input_value, expected", [
    (5, -5),
    (-7, -7),
    (0, 0),
    (3.5, -3.5),
    (-2.2, -2.2),
])
def test_make_negative_happy_path(input_value, expected):
    assert make_negative(input_value) == expected

# curto: exception - entradas não numéricas devem levantar TypeError
def test_make_negative_type_error():
    with pytest.raises(TypeError):
        make_negative("abc")
