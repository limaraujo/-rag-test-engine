import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# curto: caminho feliz ao inicializar com iterable e verificar tamanho e ponteiros
def test_init_with_iterable_happy_path():
    dl = DoubleLink([1, 2, 3])
    assert dl._length == 3
    assert dl.head is not None
    assert dl.tail is not None
    assert dl._length == len([1, 2, 3])

# curto: caso de borda com iterable vazio
def test_init_with_empty_iterable():
    dl = DoubleLink([])
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# curto: sem argumento (caso padrão)
def test_init_without_iterable():
    dl = DoubleLink()
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# curto: exceção esperada ao passar tipo não iterável
def test_init_with_non_iterable_raises_typeerror():
    with pytest.raises(TypeError):
        DoubleLink(5)
