import pytest
from repositorios.code_katas.src.sort_bylength import sort_by_length

# Verifica caminho feliz: ordena por comprimento e preserva a ordem de itens com mesmo comprimento
@pytest.mark.parametrize("input_list, expected", [
    (["aaa","b","cc","dddd","ee"], ["b","cc","ee","aaa","dddd"]),
    (["ok","to","do","no"], ["ok","to","do","no"]),
    (["","a","bb","c"], ["","a","c","bb"]),
])
def test_sort_by_length_happy_path_and_stability(input_list, expected):
    assert sort_by_length(input_list) == expected

# Verifica não mutação da entrada (retorna nova lista ordenada)
def test_sort_by_length_input_not_mutated():
    input_list = ["hello","a","bb","ccc"]
    expected_before = list(input_list)
    result = sort_by_length(input_list)
    assert input_list == expected_before
    assert result == ["a","bb","ccc","hello"]
