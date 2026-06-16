import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

def _build_list_from_string(s: str) -> DoubleLink:
    dl = DoubleLink()
    # Push characters in reverse order so that the head corresponds to the first character
    for ch in reversed(s):
        dl.push(ch)
    return dl

# Teste: caminho principal (happy path) e caso de borda simples
@pytest.mark.parametrize("s,expected", [("()", 0),("((", 1)])
def test_balanced_basic_cases(s, expected):
    dl = _build_list_from_string(s)
    assert dl.balanced() == expected

# Teste: início com ')' resulta em -1
def test_balanced_starts_with_close():
    dl = _build_list_from_string(")")
    assert dl.balanced() == -1

# Teste: lista vazia levanta ValueError
def test_balanced_empty_raises():
    dl = DoubleLink()
    with pytest.raises(ValueError):
        dl.balanced()

# Teste: valor inválido levanta ValueError
def test_balanced_invalid_value_raises():
    dl = _build_list_from_string("[")
    with pytest.raises(ValueError):
        dl.balanced()
