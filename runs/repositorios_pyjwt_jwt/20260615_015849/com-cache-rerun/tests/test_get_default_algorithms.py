import importlib
import pytest
from repositorios.pyjwt.jwt.algorithms import get_default_algorithms

def test_get_default_algorithms_without_crypto(monkeypatch):
    # verifica cenário sem suporte a criptografia externa: apenas algoritmos básicos
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    class _StubAlg:
        SHA256 = "SHA256"
        SHA384 = "SHA384"
        SHA512 = "SHA512"

        def __init__(self, *args, **kwargs):
            self.args = args

        def __repr__(self):
            return f"StubAlg{self.args}"

    monkeypatch.setattr(mod, "HMACAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "NoneAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "RSAPSSAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "OKPAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "RSAAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "ECAlgorithm", _StubAlg, raising=False)

    monkeypatch.setattr(mod, "has_crypto", False, raising=False)

    res = mod.get_default_algorithms()

    assert isinstance(res, dict)
    assert set(res.keys()) == {"none", "HS256", "HS384", "HS512"}
    for v in res.values():
        assert isinstance(v, _StubAlg)

def test_get_default_algorithms_with_crypto(monkeypatch):
    # verifica cenário com suporte a criptografia externa: RS*, ES*, PS*, EdDSA são incluídos
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    class _StubAlg:
        SHA256 = "SHA256"
        SHA384 = "SHA384"
        SHA512 = "SHA512"

        def __init__(self, *args, **kwargs):
            self.args = args

        def __repr__(self):
            return f"StubAlg{self.args}"

    monkeypatch.setattr(mod, "HMACAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "RSAAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "ECAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "RSAPSSAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "OKPAlgorithm", _StubAlg, raising=False)
    monkeypatch.setattr(mod, "NoneAlgorithm", _StubAlg, raising=False)

    for curve in ["SECP256R1", "SECP256K1", "SECP384R1", "SECP521R1"]:
        monkeypatch.setattr(mod, curve, curve, raising=False)

    monkeypatch.setattr(mod, "has_crypto", True, raising=False)

    res = mod.get_default_algorithms()

    expected_keys = {
        "none",
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
        "ES256",
        "ES256K",
        "ES384",
        "ES521",
        "ES512",
        "PS256",
        "PS384",
        "PS512",
        "EdDSA",
    }

    assert isinstance(res, dict)
    assert set(res.keys()) == expected_keys
    for v in res.values():
        assert isinstance(v, _StubAlg)
