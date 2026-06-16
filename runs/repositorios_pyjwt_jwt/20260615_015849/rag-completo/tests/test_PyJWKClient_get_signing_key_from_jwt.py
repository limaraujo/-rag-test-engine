import pytest
from types import MethodType
from unittest.mock import patch
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient



# verifica caminho feliz: decode_token retorna header com kid e get_signing_key é chamado com esse kid
def test_get_signing_key_from_jwt_happy_path_bytes():
    obj = PyJWKClient.__new__(PyJWKClient)

    expected_key = object()
    captured = {}

    def fake_get_signing_key(self, kid):
        captured['kid'] = kid
        return expected_key

    obj.get_signing_key = MethodType(fake_get_signing_key, obj)

    def fake_decode(token, options):
        captured['token'] = token
        captured['options'] = options
        return {"header": {"kid": "kid123"}}

    with patch("repositorios.pyjwt.jwt.jwks_client.decode_token", side_effect=fake_decode) as mock_decode:
        result = obj.get_signing_key_from_jwt(b"token_bytes")

    assert result is expected_key
    assert captured['token'] == b"token_bytes"
    assert captured['options'] == {"verify_signature": False}
    assert captured['kid'] == "kid123"


# verifica comportamento com kid=None no header
def test_get_signing_key_from_jwt_none_kid_bytes():
    obj = PyJWKClient.__new__(PyJWKClient)

    expected_key = object()
    captured = {}

    def fake_get_signing_key(self, kid):
        captured['kid'] = kid
        return expected_key

    obj.get_signing_key = MethodType(fake_get_signing_key, obj)

    def fake_decode(token, options):
        return {"header": {"kid": None}}

    with patch("repositorios.pyjwt.jwt.jwks_client.decode_token", side_effect=fake_decode) as mock_decode:
        result = obj.get_signing_key_from_jwt(b"token_bytes_none")

    assert result is expected_key
    assert captured['kid'] is None


# verifica suporte a token em str mantendo passagem correta do token para decode_token
def test_get_signing_key_from_jwt_with_str_token():
    obj = PyJWKClient.__new__(PyJWKClient)

    expected_key = object()
    captured = {}

    def fake_get_signing_key(self, kid):
        captured['kid'] = kid
        return expected_key

    obj.get_signing_key = MethodType(fake_get_signing_key, obj)

    def fake_decode(token, options):
        captured['token'] = token
        captured['options'] = options
        return {"header": {"kid": "str_kid"}}

    with patch("repositorios.pyjwt.jwt.jwks_client.decode_token", side_effect=fake_decode) as mock_decode:
        result = obj.get_signing_key_from_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")

    assert result is expected_key
    assert captured['token'] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    assert captured['options'] == {"verify_signature": False}
    assert captured['kid'] == "str_kid"
