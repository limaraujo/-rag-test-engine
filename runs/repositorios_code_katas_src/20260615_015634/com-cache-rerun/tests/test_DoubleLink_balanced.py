import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# curto: verifica que balancear lista vazia levanta ValueError
def test_balanced_empty_list_raises_value_error():
    dl = DoubleLink()
    with pytest.raises(ValueError) as excinfo:
        dl.balanced()
    assert "Cannot balance an empty list" in str(excinfo.value)

# curto: verifica retorno -1 quando o head é ')'
def test_balanced_head_close_paren_returns_minus_one():
    dl = DoubleLink()
    dl.push(')')
    assert dl.balanced() == -1

# curto: verifica retorno 0 para a sequência "()"
def test_balanced_happy_path_two_chars():
    dl = DoubleLink()
    dl.push(')')
    dl.push('(')
    assert dl.balanced() == 0

# curto: verifica ValueError para valor fora do conjunto permitido
def test_balanced_invalid_input_value_error():
    dl = DoubleLink()
    dl.push('x')
    with pytest.raises(ValueError) as excinfo:
        dl.balanced()
    assert "Value not in list." in str(excinfo.value)
