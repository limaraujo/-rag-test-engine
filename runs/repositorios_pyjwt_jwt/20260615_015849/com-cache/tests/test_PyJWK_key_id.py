from repositorios.pyjwt.jwt.api_jwk import PyJWK

# curto: helper para criar PyJWK sem chamar __init__
def _make_pyjwk_with_jwk(jwk_dict):
    obj = PyJWK.__new__(PyJWK)
    obj._jwk_data = jwk_dict
    return obj

# curto: happy path: kid presente como string
def test_key_id_happy_path_string():
    jwk = _make_pyjwk_with_jwk({"kid": "my-key-id"})
    assert jwk.key_id == "my-key-id"

# curto: ausência de 'kid' no dict (retorna None)
def test_key_id_missing_returns_none():
    jwk = _make_pyjwk_with_jwk({"alg": "RS256"})
    assert jwk.key_id is None

# curto: 'kid' presente com valor None (retorna None)
def test_key_id_present_none_returns_none():
    jwk = _make_pyjwk_with_jwk({"kid": None})
    assert jwk.key_id is None
