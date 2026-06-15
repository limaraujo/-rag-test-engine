from repositorios.pyjwt.jwt.api_jwk import PyJWK

def _get_key_type(jwk: PyJWK):
    """Helper to fetch key_type regardless of it being a method or a property."""
    val = getattr(jwk, "key_type")
    if callable(val):
        return val()
    return val

def test_key_type_returns_kty_when_present():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {"kty": "RSA"}
    assert _get_key_type(jwk) == "RSA"

def test_key_type_returns_none_when_missing():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {"kid": "abc"}
    assert _get_key_type(jwk) is None

def test_key_type_handles_empty_data_returns_none():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {}
    assert _get_key_type(jwk) is None
