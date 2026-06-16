import pytest
from repositorios.code_katas.src.convert import digitize

# verifica caminho feliz com múltiplos cenários válidos (happy path)
@pytest.mark.parametrize("n,expected", [
    (0, [0]),
    (5, [5]),
    (105, [5, 0, 1]),
    (12345, [5, 4, 3, 2, 1]),
])
def test_digitize_happy_path(n, expected):
    assert digitize(n) == expected

# verifica exceção para números negativos (Exceção listada)
def test_digitize_negative_raises():
    with pytest.raises(ValueError):
        digitize(-123)
