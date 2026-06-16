from repositorios.pyjwt.jwt.api_jws import PyJWS

# teste: happy path, múltiplos algoritmos suportados são retornados como lista
def test_get_algorithms_happy_path_multiple_algs():
    inst = object.__new__(PyJWS)
    inst._valid_algs = {'HS256', 'RS256'}
    algorithms = inst.get_algorithms()
    assert isinstance(algorithms, list)
    assert set(algorithms) == {'HS256', 'RS256'}
    assert len(algorithms) == 2

# teste: borda/empty, quando não há algoritmos válidos, retorna lista vazia
def test_get_algorithms_empty():
    inst = object.__new__(PyJWS)
    inst._valid_algs = set()
    algorithms = inst.get_algorithms()
    assert algorithms == []
