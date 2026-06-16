import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above

# Verifica geração da pirâmide para casos variados: caminho principal com 'ABC' e casos de borda ('', 'A')
@pytest.mark.parametrize("characters, expected", [
    ("ABC", "AAAAA\nABBBA\nABCBA\nABBBA\nAAAAA"),
    ("", ""),
    ("A", "A"),
])
def test_watch_pyramid_from_above_various(characters, expected):
    assert watch_pyramid_from_above(characters) == expected
