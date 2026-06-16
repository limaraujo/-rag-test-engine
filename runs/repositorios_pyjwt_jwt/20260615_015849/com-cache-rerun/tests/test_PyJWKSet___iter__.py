from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

def _new_pyjwkset_with_keys(keys):
    s = PyJWKSet.__new__(PyJWKSet)
    s.keys = list(keys)
    return s

# curto: happy path - verifica iteração sobre chaves não vazias na ordem correta
def test_iter_happy_path():
    s = _new_pyjwkset_with_keys([{'kid': '1'}, {'kid': '2'}, {'kid': '3'}])
    assert list(iter(s)) == s.keys

# curto: caso de borda - lista de chaves vazia retorna iterador vazio
def test_iter_empty():
    s = _new_pyjwkset_with_keys([])
    assert list(iter(s)) == []

# curto: ordem preservada entre iterações
def test_iter_preserves_order():
    items = ['a', 'b', 'c']
    s = _new_pyjwkset_with_keys(items)
    first_pass = [x for x in s]
    second_pass = [x for x in s]
    assert first_pass == items
    assert second_pass == items
    assert first_pass == second_pass
