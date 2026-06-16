import importlib
import pytest
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient

# short
# happy path: token yields a kid and signing key is returned
def test_get_signing_key_from_jwt_happy_path(monkeypatch):
    module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")
    PyJWKClient = module.PyJWKClient
    sentinel = object()
    kid_seen = {}
    calls = {}

    def fake_get_signing_key(self, kid):
        kid_seen["kid"] = kid
        return sentinel

    def fake_decode_token(token, options=None):
        calls["token"] = token
        calls["options"] = options
        return {"header": {"kid": "my-kid"}}

    monkeypatch.setattr(PyJWKClient, "get_signing_key", fake_get_signing_key, raising=True)
    monkeypatch.setattr(module, "decode_token", fake_decode_token, raising=True)

    client = PyJWKClient("https://example.com/jwks.json")
    result = client.get_signing_key_from_jwt("tokenstring")

    assert result is sentinel
    assert calls["token"] == "tokenstring"
    assert calls["options"] == {"verify_signature": False}
    assert kid_seen["kid"] == "my-kid"

# short
# missing kid in header: get_signing_key should be called with None
def test_get_signing_key_from_jwt_no_kid(monkeypatch):
    module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")
    PyJWKClient = module.PyJWKClient
    sentinel = object()
    kid_seen = {}

    def fake_get_signing_key(self, kid):
        kid_seen["kid"] = kid
        return sentinel

    def fake_decode_token(token, options=None):
        return {"header": {}}  # no kid present

    monkeypatch.setattr(PyJWKClient, "get_signing_key", fake_get_signing_key, raising=True)
    monkeypatch.setattr(module, "decode_token", fake_decode_token, raising=True)

    client = PyJWKClient("https://example.com/jwks.json")
    result = client.get_signing_key_from_jwt("tokenstring")

    assert result is sentinel
    assert kid_seen["kid"] is None

# short
# bytes token input: ensure handling of bytes payload and valid kid
def test_get_signing_key_from_jwt_bytes_token(monkeypatch):
    module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")
    PyJWKClient = module.PyJWKClient
    sentinel = object()
    kid_seen = {}

    def fake_get_signing_key(self, kid):
        kid_seen["kid"] = kid
        return sentinel

    def fake_decode_token(token, options=None):
        return {"header": {"kid": "kid-bytes"}}

    monkeypatch.setattr(PyJWKClient, "get_signing_key", fake_get_signing_key, raising=True)
    monkeypatch.setattr(module, "decode_token", fake_decode_token, raising=True)

    client = PyJWKClient("https://example.com/jwks.json")
    result = client.get_signing_key_from_jwt(b"token-bytes")

    assert result is sentinel
    assert kid_seen["kid"] == "kid-bytes"
