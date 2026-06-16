import types
from importlib import import_module
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient

# short: happy path - kid present in unverified header, decode_token called with no signature verification, key resolved
def test_get_signing_key_from_jwt_happy_path(monkeypatch):
    mod = import_module("repositorios.pyjwt.jwt.jwks_client")
    PyJWKClient = mod.PyJWKClient
    inst = object.__new__(PyJWKClient)

    kid_seen = {}
    def fake_get_signing_key(self, kid):
        kid_seen["kid"] = kid
        return {"mock": "key"}

    inst.get_signing_key = types.MethodType(fake_get_signing_key, inst)

    token = "header.payload.signature"
    decode_called = {}
    kid_value = "kid-123"
    def fake_decode_token(token_arg, options=None):
        decode_called["token"] = token_arg
        decode_called["options"] = options
        return {"header": {"kid": kid_value}}
    monkeypatch.setattr(mod, "decode_token", fake_decode_token)

    result = inst.get_signing_key_from_jwt(token)

    assert result == {"mock": "key"}
    assert kid_seen["kid"] == kid_value
    assert decode_called["token"] == token
    assert decode_called["options"] == {"verify_signature": False}

# short: missing kid - header has no kid, key lookup should receive None
def test_get_signing_key_from_jwt_missing_kid_passes_none(monkeypatch):
    mod = import_module("repositorios.pyjwt.jwt.jwks_client")
    PyJWKClient = mod.PyJWKClient
    inst = object.__new__(PyJWKClient)

    seen = {}
    def fake_get_signing_key(self, kid):
        seen["kid"] = kid
        return "ok"

    inst.get_signing_key = types.MethodType(fake_get_signing_key, inst)

    token = "token-without-kid"
    def fake_decode_token(token_arg, options=None):
        return {"header": {}}
    monkeypatch.setattr(mod, "decode_token", fake_decode_token)

    result = inst.get_signing_key_from_jwt(token)

    assert result == "ok"
    assert seen["kid"] is None

# short: token provided as bytes - ensure it passes through to decode_token and kid handling
def test_get_signing_key_from_jwt_bytes_token_preserves_input(monkeypatch):
    mod = import_module("repositorios.pyjwt.jwt.jwks_client")
    PyJWKClient = mod.PyJWKClient
    inst = object.__new__(PyJWKClient)

    kid_value = "kid-bytes"
    def fake_get_signing_key(self, kid):
        return ("ok", kid)

    inst.get_signing_key = types.MethodType(fake_get_signing_key, inst)

    token_bytes = b"header.payload.signature"
    decode_called = {}
    def fake_decode_token(token_arg, options=None):
        decode_called["token"] = token_arg
        return {"header": {"kid": kid_value}}
    monkeypatch.setattr(mod, "decode_token", fake_decode_token)

    result = inst.get_signing_key_from_jwt(token_bytes)

    assert result == ("ok", kid_value)
    assert decode_called["token"] == token_bytes
