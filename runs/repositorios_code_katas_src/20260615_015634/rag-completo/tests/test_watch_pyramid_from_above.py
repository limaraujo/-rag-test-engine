import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above

# verifica cenários não vazios (happy path) para entradas com várias letras
@pytest.mark.parametrize("characters, expected", [
    ("ABC", "AAAAA\nABBBA\nABCBA\nABBBA\nAAAAA"),
    ("AB", "AAA\nABA\nAAA"),
])
def test_watch_pyramid_from_above_non_empty(characters, expected):
    assert watch_pyramid_from_above(characters) == expected

# verifica retorno para entrada vazia
def test_watch_pyramid_from_above_empty():
    assert watch_pyramid_from_above("") == ""
