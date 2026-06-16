from repositorios.pyjwt.jwt.api_jwk import PyJWK

# Verifica retorno de key_type quando "kty" está presente (caminho feliz)
def test_key_type_happy_path():
    obj = PyJWK.__new__(PyJWK)
    obj._jwk_data = {"kty": "RSA"}
    assert obj.key_type == "RSA"

# Verifica retorno de key_type None quando não há "kty" (caso de borda)
def test_key_type_missing_returns_none():
    obj = PyJWK.__new__(PyJWK)
    obj._jwk_data = {}
    assert obj.key_type is None
