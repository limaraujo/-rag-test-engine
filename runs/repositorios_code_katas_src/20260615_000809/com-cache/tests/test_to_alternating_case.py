import pytest
from repositorios.code_katas.src.alt_case import to_alternating_case

# teste caminho feliz: casos comuns de entrada com troca de maiúsculas/minúsculas e caracteres não alfabéticos
@pytest.mark.parametrize("inp, expected", [
    ("Hello", "hELLO"),
    ("abCD123!", "ABcd123!"),
    ("", ""),
    ("Hello, World!", "hELLO, wORLD!"),
])
def test_to_alternating_case_happy_path(inp, expected):
    assert to_alternating_case(inp) == expected

# teste de exceção: entradas não-string devem levantar TypeError
@pytest.mark.parametrize("bad_input", [None, 123])
def test_to_alternating_case_raises_type_error_on_non_string_inputs(bad_input):
    with pytest.raises(TypeError):
        to_alternating_case(bad_input)
