import pytest
from repositorios.code_katas.src.alt_case import to_alternating_case

# curto: verifica caminho principal com várias entradas (happy path e bordas)
@pytest.mark.parametrize("input_str,expected", [
    ("Hello World!", "hELLO wORLD!"),
    ("to_alternating_case", "TO_ALTERNATING_CASE"),
    ("abcXYZ123!", "ABCxyz123!"),
    ("", ""),
])
def test_to_alternating_case_various(input_str, expected):
    assert to_alternating_case(input_str) == expected

# curto: verifica exceção TypeError para entradas não iteráveis
@pytest.mark.parametrize("bad_input", [None, 123])
def test_to_alternating_case_non_iterable_input_raises(bad_input):
    with pytest.raises(TypeError):
        to_alternating_case(bad_input)
