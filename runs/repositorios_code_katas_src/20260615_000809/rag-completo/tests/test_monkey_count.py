import pytest
from repositorios.code_katas.src.monkey import monkey_count

# test: variações de entrada incluindo casos de borda e cenários comuns
@pytest.mark.parametrize("n, expected", [
    (0, []),
    (1, [1]),
    (3, [1, 2, 3]),
    (5, [1, 2, 3, 4, 5]),
])
def test_monkey_count_various(n, expected):
    assert monkey_count(n) == expected
