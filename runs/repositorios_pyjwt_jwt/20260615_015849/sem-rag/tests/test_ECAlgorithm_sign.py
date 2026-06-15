import pytest
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# helper to build a minimal ECAlgorithm instance without invoking __init__
def _make_alg():
    class DummyECAlgorithm(ECAlgorithm):
        def hash_alg(self):
            return hashes.SHA256()
    alg = object.__new__(DummyECAlgorithm)
    return alg

class DummyKey:
    def __init__(self):
        self.curve = "CURVE"
        self.called = False
        self.last_msg = None
        self.last_algo = None
    def sign(self, msg, algo):
        self.called = True
        self.last_msg = msg
        self.last_algo = algo
        return b"DER_SIG"

# happy path: standard signing flow returns raw signature via der_to_raw_signature
def test_sign_happy_path(monkeypatch):
    alg = _make_alg()
    key = DummyKey()

    captured = {}

    def fake_der_to_raw_signature(der_sig, curve):
        captured['der'] = der_sig
        captured['curve'] = curve
        return b"RAW_SIG"

    monkeypatch.setattr('repositorios.pyjwt.jwt.algorithms.der_to_raw_signature', fake_der_to_raw_signature)

    result = alg.sign(b"hello", key)

    assert result == b"RAW_SIG"
    assert captured['der'] == b"DER_SIG"
    assert captured['curve'] == key.curve
    assert key.called is True
    assert isinstance(key.last_algo, ECDSA)

# exception propagation: underlying key.sign exception is not swallowed
def test_sign_propagates_exceptions(monkeypatch):
    alg = _make_alg()
    key = DummyKey()

    def raise_sign(msg, algo):
        raise ValueError("boom")

    key.sign = raise_sign

    with pytest.raises(ValueError):
        alg.sign(b"hello", key)
