import pytest
from repositorios.code_katas.src.disemvowel import disemvowel

# curto: testando disemvowel com múltiplos casos (happy path, todas vogais, sem vogais, string vazia)
@pytest.mark.parametrize("string, expected", [
    ("hello world", "hll wrld"),
    ("AEIOUaeiou", ""),
    ("rhythms", "rhythms"),
    ("", ""),
])
def test_disemvowel_parametrize(string, expected):
    assert disemvowel(string) == expected
