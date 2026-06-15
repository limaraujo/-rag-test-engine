import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side

# curto: happy path - verifica saída correta para entrada "ABC"
def test_watch_pyramid_from_the_side_happy_path():
    input_chars = "ABC"
    expected = "  C  \n BBB \nAAAAA"
    assert watch_pyramid_from_the_side(input_chars) == expected

# curto: caso de borda - entrada vazia deve retornar string vazia
def test_watch_pyramid_from_the_side_empty_string():
    assert watch_pyramid_from_the_side("") == ""

# curto: caso de borda - entrada None retorna None (comportamento falsy)
def test_watch_pyramid_from_the_side_none_input():
    assert watch_pyramid_from_the_side(None) is None

# curto: exceção explícita - entrada não-string levanta TypeError
def test_watch_pyramid_from_the_side_non_string_raises_type_error():
    with pytest.raises(TypeError):
        watch_pyramid_from_the_side(123)
