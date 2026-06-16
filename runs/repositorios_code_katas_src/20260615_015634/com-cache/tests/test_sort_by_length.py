from repositorios.code_katas.src.sort_bylength import sort_by_length

# Verifica ordenação por tamanho (caso feliz)
def test_sort_by_length_happy_path():
    arr = ["zz", "aa", "b", "ccc", "dd"]
    expected = ["b", "zz", "aa", "dd", "ccc"]
    assert sort_by_length(arr) == expected

# Verifica estabilidade: itens com mesmo comprimento preservam ordem de origem
def test_sort_by_length_stability_same_length():
    arr = ["bb", "aa", "cc", "d", "eee", "ff"]
    expected = ["d", "bb", "aa", "cc", "ff", "eee"]
    assert sort_by_length(arr) == expected

# Casos de borda: lista vazia e lista com um único elemento
def test_sort_by_length_empty_and_single():
    assert sort_by_length([]) == []
    assert sort_by_length(["x"]) == ["x"]

# Verifica ordem estável com duplicates de comprimento 1 e 2
def test_sort_by_length_duplicates_stability():
    arr = ["a", "a", "aa", "aa", "aaa"]
    expected = ["a", "a", "aa", "aa", "aaa"]
    assert sort_by_length(arr) == expected
