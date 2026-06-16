import pytest
import repositorios.pyjwt.jwt.api_jwk as jwk
from repositorios.pyjwt.jwt.api_jwk import PyJWK

# Test 1: happy path EC with P-256, algorithm inferred ES256 and key built
def test_happy_path_ec_p256_infers_es256(monkeypatch):
    # happy path: EC key, crv P-256, no explicit alg provided
    class DummyAlg:
        @classmethod
        def from_jwk(cls, jwk_data):
            return {"algorithm_class": "DummyAlg", "jwk": jwk_data}
    jwk_data = {"kty": "EC", "crv": "P-256"}
    monkeypatch.setattr(jwk, "get_default_algorithms", lambda: {"ES256": DummyAlg})
    monkeypatch.setattr(jwk, "has_crypto", False)
    monkeypatch.setattr(jwk, "requires_cryptography", set())
    obj = jwk.PyJWK(jwk_data)
    assert obj.algorithm_name == "ES256"
    assert obj.key == {"algorithm_class": "DummyAlg", "jwk": jwk_data}

# Test 2: missing kty should raise InvalidKeyError
def test_missing_kty_raises_invalid_key_error(monkeypatch):
    # missing required 'kty' field
    class DummyAlg:
        @classmethod
        def from_jwk(cls, jwk_data):
            return {"algorithm_class": "DummyAlg", "jwk": jwk_data}
    jwk_data = {"crv": "P-256"}
    monkeypatch.setattr(jwk, "get_default_algorithms", lambda: {"ES256": DummyAlg})
    monkeypatch.setattr(jwk, "has_crypto", True)
    monkeypatch.setattr(jwk, "requires_cryptography", set())
    with pytest.raises(jwk.InvalidKeyError):
        jwk.PyJWK(jwk_data)

# Test 3: OKP Ed25519 yields EdDSA and builds key
def test_okp_ed25519_infers_eddsa(monkeypatch):
    # OKP with Ed25519 should infer EdDSA
    class DummyAlg:
        @classmethod
        def from_jwk(cls, jwk_data):
            return {"algorithm_class": "DummyAlg", "jwk": jwk_data}
    jwk_data = {"kty": "OKP", "crv": "Ed25519"}
    monkeypatch.setattr(jwk, "get_default_algorithms", lambda: {"EdDSA": DummyAlg})
    monkeypatch.setattr(jwk, "has_crypto", False)
    monkeypatch.setattr(jwk, "requires_cryptography", set())
    obj = jwk.PyJWK(jwk_data)
    assert obj.algorithm_name == "EdDSA"
    assert obj.key == {"algorithm_class": "DummyAlg", "jwk": jwk_data}

# Test 4: missing cryptography dependency raises MissingCryptographyError
def test_missing_cryptography_raises(monkeypatch):
    # encryption algorithm requires cryptography and is unavailable
    class DummyAlg:
        @classmethod
        def from_jwk(cls, jwk_data):
            return {"algorithm_class": "DummyAlg", "jwk": jwk_data}
    jwk_data = {"kty": "EC", "crv": "P-256"}  # would infer ES256
    monkeypatch.setattr(jwk, "get_default_algorithms", lambda: {"ES256": DummyAlg})
    monkeypatch.setattr(jwk, "has_crypto", False)
    monkeypatch.setattr(jwk, "requires_cryptography", {"ES256"})
    with pytest.raises(jwk.MissingCryptographyError):
        jwk.PyJWK(jwk_data)
