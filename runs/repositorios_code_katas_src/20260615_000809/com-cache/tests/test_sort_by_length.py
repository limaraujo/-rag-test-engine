import pytest
from repositorios.code_katas.src.sort_bylength import sort_by_length

# verifica caminho principal: ordena por comprimento e mantém ordem estável entre mesmas larguras
@pytest.mark.parametrize("arr, expected", [
    (["a","abcd","ab",""], ["","a","ab","abcd"]),
    (["aa","bb","c","d"], ["c","d","aa","bb"]),
])
def test_sort_by_length_basic_happy_path(arr, expected):
    assert sort_by_length(arr) == expected

# verifica exceção TypeError quando elementos não possuem len
def test_sort_by_length_raises_type_error_on_non_string():
    with pytest.raises(TypeError):
        sort_by_length(["a", 2, "bbb"])
