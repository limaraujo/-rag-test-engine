import pytest
from repositorios.code_katas.src.disemvowel import disemvowel

# Verifica remoção de vogais em entradas variadas (happy path, bordas, pontuação)
@pytest.mark.parametrize("input_string, expected", [
    ("hello world", "hll wrld"),
    ("Quick brown fox.", "Qck brwn fx."),
    ("aeiouAEIOU", ""),
    ("", ""),
    ("h@llo!", "h@ll!")
])
def test_disemvowel_basic_cases(input_string, expected):
    assert disemvowel(input_string) == expected
