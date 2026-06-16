import pytest
from repositorios.code_katas.src.disemvowel import disemvowel

# verifica remoção de vogais (caminho feliz e bordas) para várias entradas
@pytest.mark.parametrize("input_str, expected", [
    ("hello", "hll"),
    ("world", "wrld"),
    ("HELLO", "HLL"),
    ("1234!?", "1234!?"),
    ("aeiouAEIOU", "")
])
def test_disemvowel_various_cases(input_str, expected):
    assert disemvowel(input_str) == expected
