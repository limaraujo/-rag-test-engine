import importlib
import pytest
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# Load module to patch internal dependencies
mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")


# happy path: verifies ECAlgorithm.sign uses ECDSA with hash_alg and returns the raw signature
def test_happy_path_sign_returns_raw_signature(monkeypatch):
    captured = {}

    def fake_ECDSA(hash_alg):
        captured["hash_alg"] = hash_alg
        return "ECDSA_SENTINEL"

    def fake_der_to_raw_signature(der_sig, curve):
        captured["der_sig"] = der_sig
        captured["curve"] = curve
        return b"RAW_SIG"

    def fixed_hash_alg(self):
        return "HASH_ALG"

    monkeypatch.setattr(mod, "ECDSA", fake_ECDSA, raising=True)
    monkeypatch.setattr(mod, "der_to_raw_signature", fake_der_to_raw_signature, raising=True)
    monkeypatch.setattr(ECAlgorithm, "hash_alg", fixed_hash_alg, raising=False)

    class DummyKey:
        def __init__(self):
            self.curve = "CURVE"
            self.sign_called_with = None

        def sign(self, msg, sig_alg):
            self.sign_called_with = (msg, sig_alg)
            return b"DER_SIG"

    algo = ECAlgorithm(hash_alg=lambda: "HASH_ALG")
    key = DummyKey()

    result = algo.sign(b"MSG", key)

    assert result == b"RAW_SIG"
    assert key.sign_called_with == (b"MSG", "ECDSA_SENTINEL")
    assert captured.get("hash_alg") == "HASH_ALG"
    assert captured.get("der_sig") == b"DER_SIG"
    assert captured.get("curve") == "CURVE"


# exception path: ensure ValueError from key.sign propagates
def test_sign_propagates_exception_from_key_sign(monkeypatch):
    captured = {}

    def fake_ECDSA(hash_alg):
        captured["hash_alg"] = hash_alg
        return "ECDSA_SENTINEL"

    def fixed_hash_alg(self):
        return "HASH_ALG"

    def fake_der_to_raw_signature(der_sig, curve):
        captured["der_sig"] = der_sig
        captured["curve"] = curve
        return b"RAW_SIG"

    monkeypatch.setattr(mod, "ECDSA", fake_ECDSA, raising=True)
    monkeypatch.setattr(mod, "der_to_raw_signature", fake_der_to_raw_signature, raising=True)
    monkeypatch.setattr(ECAlgorithm, "hash_alg", fixed_hash_alg, raising=False)

    class DummyKeyRaise:
        def __init__(self):
            self.curve = "CURVE"

        def sign(self, msg, sig_alg):
            raise ValueError("bad key")

    algo = ECAlgorithm(hash_alg=lambda: "HASH_ALG")
    key = DummyKeyRaise()

    with pytest.raises(ValueError, match="bad key"):
        algo.sign(b"MSG", key)


# exception path: der_to_raw_signature raises, ensure propagation
def test_sign_propagates_exception_from_der_to_raw_signature(monkeypatch):
    def fake_ECDSA(hash_alg):
        return "ECDSA_SENTINEL"

    def fixed_hash_alg(self):
        return "HASH_ALG"

    def fake_der_to_raw_signature(der_sig, curve):
        raise RuntimeError("der error")

    monkeypatch.setattr(mod, "ECDSA", fake_ECDSA, raising=True)
    monkeypatch.setattr(mod, "der_to_raw_signature", fake_der_to_raw_signature, raising=True)
    monkeypatch.setattr(ECAlgorithm, "hash_alg", fixed_hash_alg, raising=False)

    class DummyKey:
        def __init__(self):
            self.curve = "CURVE"

        def sign(self, msg, sig_alg):
            return b"DER_SIG"

    algo = ECAlgorithm(hash_alg=lambda: "HASH_ALG")
    key = DummyKey()

    with pytest.raises(RuntimeError, match="der error"):
        algo.sign(b"MSG", key)
