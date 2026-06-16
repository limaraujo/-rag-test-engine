import pytest
from repositorios.code_katas.src.convert import digitize

# Verifica que digitize retorna dígitos invertidos para inteiros não negativos (casos felizes)
@pytest.mark.parametrize("n,expected", [
    (0, [0]),
    (3, [3]),
    (123, [3, 2, 1]),
    (100, [0, 0, 1]),
])
def test_digitize_non_negative_integers(n, expected):
    assert digitize(n) == expected

# Verifica que digitize levanta ValueError para números negativos
def test_digitize_negative_raises_value_error():
    with pytest.raises(ValueError):
        digitize(-12)
