from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# happy path: retorna o jwk_set exatamente como armazenado
def test_get_jwk_set_happy_path():
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    sentinel = {"kty": "oct", "k": "test"}
    inst.jwk_set = sentinel
    assert inst.get_jwk_set() is sentinel

# borda: jwk_set é None
def test_get_jwk_set_none():
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    inst.jwk_set = None
    assert inst.get_jwk_set() is None

# atualização/reflection: alterações em jwk_set são refletidas na saída
def test_get_jwk_set_mutation_reflects_change():
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    first = {"a": 1}
    inst.jwk_set = first
    assert inst.get_jwk_set() is first
    second = {"a": 2}
    inst.jwk_set = second
    assert inst.get_jwk_set() is second
