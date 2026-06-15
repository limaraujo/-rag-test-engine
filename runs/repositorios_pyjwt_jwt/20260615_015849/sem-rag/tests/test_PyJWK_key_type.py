from repositorios.pyjwt.jwt.api_jwk import PyJWK

def test_key_type_returns_value_when_present():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {"kty": "RSA"}
    assert jwk.key_type == "RSA"

def test_key_type_returns_none_when_missing():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {"use": "sig"}
    assert jwk.key_type is None

def test_key_type_returns_none_when_explicit_none():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {"kty": None}
    assert jwk.key_type is None
