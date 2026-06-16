from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# happy path: returns the exact jwk_set object stored on the instance
def test_get_jwk_set_happy_path_returns_same_object():
    instance = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    jwk_set = object()
    instance.jwk_set = jwk_set
    assert instance.get_jwk_set() is jwk_set

# edge case: jwk_set is None returns None
def test_get_jwk_set_returns_none_when_jwk_set_is_none():
    instance = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    instance.jwk_set = None
    assert instance.get_jwk_set() is None
