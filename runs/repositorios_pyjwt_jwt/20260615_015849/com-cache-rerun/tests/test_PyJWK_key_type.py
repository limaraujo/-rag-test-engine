from repositorios.pyjwt.jwt.api_jwk import PyJWK


def _make_jwk_with_data(jwk_data):
    obj = PyJWK.__new__(PyJWK)
    obj._jwk_data = jwk_data
    return obj


def _get_key_type(jwk):
    key_type = getattr(jwk, "key_type")
    return key_type() if callable(key_type) else key_type


def test_key_type_happy_path():
    jwk = _make_jwk_with_data({"kty": "RSA"})
    assert _get_key_type(jwk) == "RSA"


def test_key_type_missing_kty():
    jwk = _make_jwk_with_data({})
    assert _get_key_type(jwk) is None


def test_key_type_none_value():
    jwk = _make_jwk_with_data({"kty": None})
    assert _get_key_type(jwk) is None
