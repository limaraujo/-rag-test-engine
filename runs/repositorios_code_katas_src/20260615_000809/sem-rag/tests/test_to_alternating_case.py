import pytest
from repositorios.code_katas.src.alt_case import to_alternating_case

# Verifica o caminho principal (happy path) com várias entradas via parametrização
@pytest.mark.parametrize("input_str, expected", [
    ("Hello World", "hELLO wORLD"),
    ("", ""),
    ("123abcXYZ!", "123ABCxyz!"),
    ("áé", "ÁÉ"),
    ("ß", "SS"),
])
def test_to_alternating_case_happy_path(input_str, expected):
    assert to_alternating_case(input_str) == expected

# Verifica exceção para entrada não-iterável (TypeError)
def test_to_alternating_case_invalid_input_type_error():
    with pytest.raises(TypeError):
        to_alternating_case(None)
