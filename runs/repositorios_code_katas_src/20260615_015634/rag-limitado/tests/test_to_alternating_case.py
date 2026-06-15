import pytest
from repositorios.code_katas.src.alt_case import to_alternating_case

# curto: happy path com variados cenários comuns (maiúsculas/minúsculas, espaços e pontuação)
@pytest.mark.parametrize("input_str,expected", [
    ("Hello-World", "hELLO-wORLD"),
    ("abCD", "ABcd"),
    ("123abc!", "123ABC!"),
    ("Hello, World!", "hELLO, wORLD!")
])
def test_to_alternating_case_happy_paths(input_str, expected):
    assert to_alternating_case(input_str) == expected

# curto: caso input não iterável deve levantar TypeError
def test_to_alternating_case_raises_type_error_on_non_iterable():
    with pytest.raises(TypeError):
        to_alternating_case(5)
