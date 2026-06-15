from repositorios.pyjwt.jwt.api_jwk import PyJWK

def _make_jwk_with_data(data: dict) -> PyJWK:
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = data
    return jwk

# Verifica retorno value quando 'use' está presente (happy path)
def test_public_key_use_returns_value_when_present():
    jwk = _make_jwk_with_data({"use": "sig"})
    assert jwk.public_key_use == "sig"

# Verifica retorno None quando a chave 'use' está ausente
def test_public_key_use_none_when_missing():
    jwk = _make_jwk_with_data({})
    assert jwk.public_key_use is None

# Verifica retorno None quando o valor de 'use' é None
def test_public_key_use_none_when_none_value():
    jwk = _make_jwk_with_data({"use": None})
    assert jwk.public_key_use is None
