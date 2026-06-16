import pytest
import importlib
from repositorios.pyjwt.jwt.api_jwk import PyJWK

api_jwk = importlib.import_module("repositorios.pyjwt.jwt.api_jwk")

InvalidKeyError = getattr(api_jwk, "InvalidKeyError")
PyJWKError = getattr(api_jwk, "PyJWKError")


def test_pyjwk_init_happy_path_rsa_with_alg(monkeypatch):
    class DummyAlg:
        @classmethod
        def from_jwk(cls, jwk):
            return {"algorithm": "RS256_from_jwk", "jwk": jwk}

    monkeypatch.setattr(api_jwk, "get_default_algorithms", lambda: {"RS256": DummyAlg})
    monkeypatch.setattr(api_jwk, "has_crypto", True, raising=False)

    jwk = {"kty": "RSA", "n": "dummy", "e": "AQAB", "alg": "RS256"}
    obj = PyJWK(jwk)

    assert obj.algorithm_name == "RS256"
    assert obj.key == {"algorithm": "RS256_from_jwk", "jwk": jwk}
    assert obj._jwk_data == jwk


def test_pyjwk_init_missing_kty_raises_invalidkey():
    jwk = {"alg": "RS256"}
    with pytest.raises(InvalidKeyError):
        PyJWK(jwk)


def test_pyjwk_init_ec_invalid_crv_raises_invalidkey():
    jwk = {"kty": "EC", "crv": "not-a-crv"}
    with pytest.raises(InvalidKeyError):
        PyJWK(jwk)


def test_pyjwk_init_pyjwkerror_if_algorithm_missing_in_algorithms(monkeypatch):
    class DummyAlg:
        @classmethod
        def from_jwk(cls, jwk):
            return {"algorithm": "UNKNOWN_from_jwk", "jwk": jwk}

    jwk = {"kty": "RSA", "alg": "RS512"}

    monkeypatch.setattr(api_jwk, "has_crypto", True, raising=False)
    monkeypatch.setattr(api_jwk, "get_default_algorithms", lambda: {"RS256": DummyAlg})

    with pytest.raises(PyJWKError):
        PyJWK(jwk)
