from unittest.mock import Mock
import pytest
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient

from unittest.mock import Mock

import pytest
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient



# Testa caminho feliz: kid presente no token é repassado para get_signing_key e retorna a chave
def test_get_signing_key_from_jwt_happy_path(monkeypatch):
    # arrange
    client = PyJWKClient.__new__(PyJWKClient)
    kid = "kid-abc"
    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.jwks_client.decode_token",
        lambda token, options=None: {"header": {"kid": kid}},
    )
    signer = Mock(return_value="SIGNING_KEY_ABC")
    client.get_signing_key = signer

    # act
    result = PyJWKClient.get_signing_key_from_jwt(client, "token_string")

    # assert
    assert result == "SIGNING_KEY_ABC"
    signer.assert_called_once_with(kid)


# Testa que decode_token é chamado com verify_signature=False
def test_get_signing_key_from_jwt_calls_decode_with_no_verify(monkeypatch):
    client = PyJWKClient.__new__(PyJWKClient)
    kid = "kid-no-verify"
    def decode_spy(token, options=None):
        assert options == {"verify_signature": False}
        return {"header": {"kid": kid}}
    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.jwks_client.decode_token",
        decode_spy,
    )
    signer = Mock(return_value="KEY_NO_VERIFY")
    client.get_signing_key = signer

    PyJWKClient.get_signing_key_from_jwt(client, "token_string")

    signer.assert_called_once_with(kid)


# Testa caso borda: kid é None no header do token
def test_get_signing_key_from_jwt_none_kid(monkeypatch):
    client = PyJWKClient.__new__(PyJWKClient)
    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.jwks_client.decode_token",
        lambda token, options=None: {"header": {"kid": None}},
    )
    signer = Mock(return_value="KEY_NONE")
    client.get_signing_key = signer

    result = PyJWKClient.get_signing_key_from_jwt(client, "token_string")

    signer.assert_called_once_with(None)
    assert result == "KEY_NONE"
