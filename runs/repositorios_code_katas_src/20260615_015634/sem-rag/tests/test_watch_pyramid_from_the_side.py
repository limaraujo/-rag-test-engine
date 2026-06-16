import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side

# verifica retorno em cenários com entrada vazia, caractere único, dois e três caracteres
@pytest.mark.parametrize("characters, expected", [
    ("", ""),
    ("X", "X"),
    ("AB", " B \nAAA"),
    ("ABC", "  C  \n BBB \nAAAAA"),
])
def test_watch_pyramid_from_side_various_inputs(characters, expected):
    assert watch_pyramid_from_the_side(characters) == expected
