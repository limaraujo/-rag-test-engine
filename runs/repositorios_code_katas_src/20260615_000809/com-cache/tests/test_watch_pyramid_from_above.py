import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above

# Verifica watch_pyramid_from_above com múltiplos casos: caminho feliz para AB/ABC, e casos de borda (vazio, None)
@pytest.mark.parametrize("characters, expected", [
    ("", ""),
    (None, None),
    ("AB", "AAA\nABA\nAAA"),
    ("ABC", "AAAAA\nABBBA\nABCBA\nABBBA\nAAAAA"),
])
def test_watch_pyramid_from_above_various_inputs(characters, expected):
    assert watch_pyramid_from_above(characters) == expected

# Verifica exceção esperada quando input não é iterável (integer)
def test_watch_pyramid_from_above_raises_with_non_iterable():
    # caso de borda: entrada não iterável deve levantar TypeError
    with pytest.raises(TypeError):
        watch_pyramid_from_above(123)
