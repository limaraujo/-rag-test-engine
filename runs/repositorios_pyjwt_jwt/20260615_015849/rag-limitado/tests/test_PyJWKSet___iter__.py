import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

# curto: testa o caminho feliz quando keys é uma lista; __iter__ deve devolver os elementos na ordem correta
class _TestPyJWKSet(PyJWKSet):
    def __init__(self, keys):
        self.keys = keys

# curto: confirmar que iterar sobre um PyJWKSet com keys como lista respeita a ordem
def test_iter_happy_path_yields_elements_in_order():
    # Arrange
    s = _TestPyJWKSet(keys=[1, 2, 3])
    # Act
    it = iter(s)
    result = list(it)
    # Assert
    assert result == [1, 2, 3]

# curto: testar o caso em que keys é um iterator; __iter__ deve retornar o mesmo iterator
def test_iter_with_keys_as_iterator_returns_same_iterator():
    # Arrange
    keys_iter = iter([10, 20, 30])
    s = _TestPyJWKSet(keys=keys_iter)
    # Act
    it = iter(s)
    # Assert
    assert it is keys_iter
    assert next(it) == 10
    assert next(it) == 20
    assert next(it) == 30
    with pytest.raises(StopIteration):
        next(it)
