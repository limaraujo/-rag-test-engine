from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# happy path: retorna exatamente o objeto atribuído a jwk_set
def test_get_jwk_set_happy_path_returns_same_object():
    inst = object.__new__(PyJWTSetWithTimestamp)
    dummy = {"kty": "RSA", "kid": "abc"}
    inst.jwk_set = dummy
    assert inst.get_jwk_set() is dummy

# borda: jwk_set é None
def test_get_jwk_set_none_returns_none():
    inst = object.__new__(PyJWTSetWithTimestamp)
    inst.jwk_set = None
    assert inst.get_jwk_set() is None

# caso de borda/versão mutável: retorna a mesma referência
def test_get_jwk_set_returns_same_mutable_reference():
    inst = object.__new__(PyJWTSetWithTimestamp)
    lst = []
    inst.jwk_set = lst
    result = inst.get_jwk_set()
    assert result is lst
    lst.append("updated")
    assert result == ["updated"]
