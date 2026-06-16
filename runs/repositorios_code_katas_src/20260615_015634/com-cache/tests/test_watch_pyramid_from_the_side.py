import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side


# curto
def test_watch_pyramid_from_the_side_three_characters():
    # verifica caminho feliz com entrada 'abc'
    input_chars = "abc"
    expected = "  c  \n bbb \naaaaa"
    assert watch_pyramid_from_the_side(input_chars) == expected

# curto
def test_watch_pyramid_from_the_side_empty_string():
    # verifica caso de borda: entrada vazia retorna vazia
    assert watch_pyramid_from_the_side("") == ""

# curto
def test_watch_pyramid_from_the_side_four_characters():
    # verifica caminho feliz com entrada 'abcd'
    input_chars = "abcd"
    expected = "   d   \n  ccc  \n bbbbb \naaaaaaa"
    assert watch_pyramid_from_the_side(input_chars) == expected
