import importlib
import pytest
from repositorios.pyjwt.jwt.algorithms import get_default_algorithms

# short: verifica estado sem crypto (branch else) — apenas chaves básicas
def test_get_default_algorithms_without_crypto(monkeypatch):
    algos = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    # mocks simples para evitar dependências de crypto
    class DummyAlgo:
        SHA256 = "SHA256"
        SHA384 = "SHA384"
        SHA512 = "SHA512"
        def __init__(self, *args):
            self.args = args

    monkeypatch.setattr(algos, "NoneAlgorithm", lambda: "NONE", raising=True)
    monkeypatch.setattr(algos, "HMACAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "RSAAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "ECAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "RSAPSSAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "OKPAlgorithm", DummyAlgo, raising=True)

    monkeypatch.setattr(algos, "SECP256R1", "SECP256R1", raising=False)
    monkeypatch.setattr(algos, "SECP256K1", "SECP256K1", raising=False)
    monkeypatch.setattr(algos, "SECP384R1", "SECP384R1", raising=False)
    monkeypatch.setattr(algos, "SECP521R1", "SECP521R1", raising=False)

    monkeypatch.setattr(algos, "has_crypto", False, raising=False)

    result = algos.get_default_algorithms()

    assert isinstance(result, dict)
    assert set(result.keys()) == {"none", "HS256", "HS384", "HS512"}

# short: verifica branch com crypto ativado e valida chaves e argumentos esperados
def test_get_default_algorithms_with_crypto_includes_expected_keys_and_args(monkeypatch):
    algos = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    class DummyAlgo:
        SHA256 = "SHA256"
        SHA384 = "SHA384"
        SHA512 = "SHA512"
        def __init__(self, *args):
            self.args = args

    # Instala mocks
    monkeypatch.setattr(algos, "NoneAlgorithm", lambda: "NONE", raising=True)
    monkeypatch.setattr(algos, "HMACAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "RSAAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "ECAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "RSAPSSAlgorithm", DummyAlgo, raising=True)
    monkeypatch.setattr(algos, "OKPAlgorithm", DummyAlgo, raising=True)

    # curvas/ferramentas usadas na criação de algoritmos EC/RSA
    monkeypatch.setattr(algos, "SECP256R1", "SECP256R1", raising=False)
    monkeypatch.setattr(algos, "SECP256K1", "SECP256K1", raising=False)
    monkeypatch.setattr(algos, "SECP384R1", "SECP384R1", raising=False)
    monkeypatch.setattr(algos, "SECP521R1", "SECP521R1", raising=False)

    # simula disponibilidade de crypto
    monkeypatch.setattr(algos, "has_crypto", True, raising=False)

    result = algos.get_default_algorithms()

    expected_keys = {
        "none", "HS256", "HS384", "HS512",
        "RS256", "RS384", "RS512",
        "ES256", "ES256K", "ES384", "ES521", "ES512",
        "PS256", "PS384", "PS512",
        "EdDSA",
    }

    assert isinstance(result, dict)
    assert set(result.keys()) == expected_keys

    # verifica argumentos esperados para alguns casos
    assert isinstance(result["RS256"], DummyAlgo)
    assert result["RS256"].args == ("SHA256",)

    assert isinstance(result["ES256"], DummyAlgo)
    assert result["ES256"].args == ("SHA256", "SECP256R1")

    assert isinstance(result["ES256K"], DummyAlgo)
    assert result["ES256K"].args == ("SHA256", "SECP256K1")

    assert isinstance(result["ES512"], DummyAlgo)
    assert result["ES512"].args == ("SHA512", "SECP521R1")

    assert isinstance(result["PS256"], DummyAlgo)
    assert result["PS256"].args == ("SHA256",)

    assert isinstance(result["EdDSA"], DummyAlgo)
    assert result["EdDSA"].args == ()
