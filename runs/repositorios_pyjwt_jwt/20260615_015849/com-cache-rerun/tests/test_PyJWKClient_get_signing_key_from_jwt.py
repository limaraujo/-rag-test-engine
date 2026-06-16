import importlib
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient


# helper to create an uninitialized PyJWKClient instance
def _make_client():
    return object.__new__(PyJWKClient)

# DICA: happy path - kid presente no header deve ser utilizado para obter a chave
def test_get_signing_key_from_jwt_happy_path(monkeypatch):
    jwks_module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")

    def fake_decode_token(token, options=None):
        return {"header": {"kid": "kid-123"}}

    client = _make_client()

    monkeypatch.setattr(jwks_module, "decode_token", fake_decode_token)
    monkeypatch.setattr(client, "get_signing_key", lambda kid: f"signing-key-{kid}")

    result = PyJWKClient.get_signing_key_from_jwt(client, b"some-token")
    assert result == "signing-key-kid-123"

# DICA: ausência de kid no header - deve chamar get_signing_key com None
def test_get_signing_key_from_jwt_missing_kid_calls_with_none(monkeypatch):
    jwks_module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")

    def fake_decode_token(token, options=None):
        return {"header": {}}

    client = _make_client()

    monkeypatch.setattr(jwks_module, "decode_token", fake_decode_token)
    captured = {}
    def fake_get_signing_key(kid):
        captured["kid"] = kid
        return "default-key"

    monkeypatch.setattr(client, "get_signing_key", fake_get_signing_key)

    result = PyJWKClient.get_signing_key_from_jwt(client, "token")
    assert result == "default-key"
    assert captured["kid"] is None

# DICA: suporte a token str/bytes indiferente - validação básica de fluxo
def test_get_signing_key_from_jwt_accepts_str_token(monkeypatch):
    jwks_module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")

    def fake_decode_token(token, options=None):
        assert isinstance(token, (str, bytes))
        return {"header": {"kid": "abc"}}

    client = _make_client()

    monkeypatch.setattr(jwks_module, "decode_token", fake_decode_token)
    monkeypatch.setattr(client, "get_signing_key", lambda kid: f"key-{kid}")

    result = PyJWKClient.get_signing_key_from_jwt(client, "token-string")
    assert result == "key-abc"
