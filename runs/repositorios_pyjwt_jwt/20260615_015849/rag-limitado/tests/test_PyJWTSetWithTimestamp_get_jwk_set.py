from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

def test_get_jwk_set_returns_internal_value_happy_path():
    # happy path: returns the internal jwk_set object
    jwk = {"kty": "RSA"}
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    inst.jwk_set = jwk
    assert inst.get_jwk_set() is jwk

def test_get_jwk_set_returns_none_when_not_set():
    # edge case: jwk_set is None; method should return None
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    inst.jwk_set = None
    assert inst.get_jwk_set() is None
