import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS


# curto: happy path - retorna a lista exatamente como os algoritmos fornecidos, mantendo a ordem
def test_get_algorithms_happy_path_preserves_order():
    inst = PyJWS.__new__(PyJWS)
    inst._valid_algs = ['HS256', 'RS256', 'ES256']
    assert inst.get_algorithms() == ['HS256', 'RS256', 'ES256']

# curto: caso de borda/entrada imutável (tuple) - deve converter para list mantendo ordem
def test_get_algorithms_with_tuple_input_converts_to_list():
    inst = PyJWS.__new__(PyJWS)
    inst._valid_algs = ('HS256', 'RS256')
    assert inst.get_algorithms() == ['HS256', 'RS256']

# curto: caso de borda - entrada vazia deve retornar lista vazia
def test_get_algorithms_with_empty_input_returns_empty_list():
    inst = PyJWS.__new__(PyJWS)
    inst._valid_algs = []
    assert inst.get_algorithms() == []
