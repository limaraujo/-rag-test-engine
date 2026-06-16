import pytest
from repositorios.code_katas.src.sort_bylength import sort_by_length

# testa sorting por comprimento para múltiplos cenários (happy path, lista vazia, estabilidade)
@pytest.mark.parametrize("arr,expected", [
    (["a","bb","ccc","dd"], ["a","bb","dd","ccc"]),
    ([], []),
    (["aa","bb","cc","d"], ["d","aa","bb","cc"]),
    (["longer","short","mid"], ["mid","short","longer"]),
])
def test_sort_by_length_various_cases(arr, expected):
    assert sort_by_length(arr) == expected

# verifica comportamento com entrada contendo elementos não-string (exceção TypeError esperada)
def test_type_error_on_non_string_input():
    with pytest.raises(TypeError):
        sort_by_length([1, "a"])
