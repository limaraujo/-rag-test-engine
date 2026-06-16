import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# Borda: lista vazia levanta ValueError
def test_balanced_empty_list_raises_value_error():
    dl = DoubleLink()
    with pytest.raises(ValueError) as exc:
        dl.balanced()
    assert "empty" in str(exc.value).lower()

# Caminho principal/Exceção: primeiro nó é ')' => retorna -1
def test_balanced_single_closing_paren_returns_minus_one():
    dl = DoubleLink()
    dl.push(")")
    assert dl.balanced() == -1

# Ramificação: '(' seguido por símbolo diferente de ')' => retorna 1
def test_balanced_open_followed_by_other_symbol_branch_returns_one():
    dl = DoubleLink()
    dl.push("[")  # cria tail
    dl.push("(")  # head; lista: "(" -> "["
    assert dl.balanced() == 1

# Exceção: valor não reconhecido no nó superior levanta ValueError
def test_balanced_invalid_input_raises_value_error():
    dl = DoubleLink()
    dl.push("x")
    with pytest.raises(ValueError) as exc:
        dl.balanced()
    assert "Value not in list" in str(exc.value)
