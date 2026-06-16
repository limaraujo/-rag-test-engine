from cryptography.exceptions import InvalidSignature
import pytest
import repositorios.pyjwt.jwt.algorithms as algo_mod
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm

class DummyHash:
    digest_size = 32

class DummyMGF1:
    def __init__(self, hash_alg):
        self.hash_alg = hash_alg

class DummyPSS:
    def __init__(self, mgf, salt_length):
        self.mgf = mgf
        self.salt_length = salt_length

class FakeKey:
    def __init__(self, raise_exc=None):
        self.raise_exc = raise_exc
        self.args = None
    def verify(self, sig, msg, padding_obj, hash_alg_obj):
        self.args = (sig, msg, padding_obj, hash_alg_obj)
        if self.raise_exc:
            raise self.raise_exc
        return None

# happy path: signature is valid, verify returns True
# happy path: valid signature scenario
def test_verify_happy_path(monkeypatch):
    monkeypatch.setattr(algo_mod.padding, 'MGF1', DummyMGF1)
    monkeypatch.setattr(algo_mod.padding, 'PSS', DummyPSS)

    inst = object.__new__(RSAPSSAlgorithm)
    inst.hash_alg = lambda: DummyHash()

    key = FakeKey()
    result = inst.verify(b"hello", key, b"sig")

    assert result is True
    sig, msg, padding_obj, hash_alg_obj = key.args
    assert sig == b"sig"
    assert msg == b"hello"
    assert isinstance(padding_obj, DummyPSS)
    assert isinstance(hash_alg_obj, DummyHash)

# invalid signature: key.verify raises InvalidSignature -> verify should return False
# exception handling path
def test_verify_invalid_signature_returns_false(monkeypatch):
    monkeypatch.setattr(algo_mod.padding, 'MGF1', DummyMGF1)
    monkeypatch.setattr(algo_mod.padding, 'PSS', DummyPSS)

    inst = object.__new__(RSAPSSAlgorithm)
    inst.hash_alg = lambda: DummyHash()

    key = FakeKey(raise_exc=InvalidSignature())
    result = inst.verify(b"hello", key, b"sig")

    assert result is False

# other exception propagates: verify should not swallow non-InvalidSignature exceptions
# error propagation path
def test_verify_propagates_other_exceptions(monkeypatch):
    monkeypatch.setattr(algo_mod.padding, 'MGF1', DummyMGF1)
    monkeypatch.setattr(algo_mod.padding, 'PSS', DummyPSS)

    inst = object.__new__(RSAPSSAlgorithm)
    inst.hash_alg = lambda: DummyHash()

    key = FakeKey(raise_exc=ValueError("boom"))
    with pytest.raises(ValueError):
        inst.verify(b"hello", key, b"sig")
