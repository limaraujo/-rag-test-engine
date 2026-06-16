import pytest
from repositorios.code_katas.src.return_negative import make_negative

# happy path: número positivo -> negativo do valor absoluto
def test_make_negative_positive():
    assert make_negative(5) == -5

# happy path: número negativo -> retorna o mesmo valor negativo (que já é negativo)
def test_make_negative_negative():
    assert make_negative(-7) == -7

# edge case: zero -> zero
def test_make_negative_zero():
    assert make_negative(0) == 0

# raises: entrada não numérica gera TypeError
def test_make_negative_invalid_type_raises_type_error():
    with pytest.raises(TypeError):
        make_negative("a")
