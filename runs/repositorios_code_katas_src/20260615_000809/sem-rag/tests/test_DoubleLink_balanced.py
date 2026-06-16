import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

def _add(dl, value):
    # tenta métodos comuns de append
    for method in ("append", "push", "add"):
        if hasattr(dl, method):
            getattr(dl, method)(value)
            return
    raise AttributeError("DoubleLink tem que oferecer append/push/add para adicionar valores")

# happy path: caminho principal com parênteses balanceados "()"
def test_balanced_happy_path():
    dl = DoubleLink()
    _add(dl, "(")
    _add(dl, ")")
    assert dl.balanced() == -1

# borda: lista vazia deve levantar ValueError
def test_balanced_empty_list_raises_value_error():
    dl = DoubleLink()
    with pytest.raises(ValueError):
        dl.balanced()

# borda: entrada inválida (valor não suportado) deve levantar ValueError
def test_balanced_invalid_input_raises_value_error():
    dl = DoubleLink()
    _add(dl, "x")
    with pytest.raises(ValueError):
        dl.balanced()

# branch: cabeça é ')', retornar -1 (unmatched closed paren)
def test_balanced_head_closing_returns_minus_one():
    dl = DoubleLink()
    _add(dl, ")")
    assert dl.balanced() == -1
