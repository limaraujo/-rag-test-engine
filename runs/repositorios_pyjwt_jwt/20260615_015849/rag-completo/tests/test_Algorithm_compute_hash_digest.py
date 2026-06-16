import hashlib
import pytest
import repositorios.pyjwt.jwt.algorithms as alg_mod
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes as crypto_hashes
from repositorios.pyjwt.jwt.algorithms import Algorithm

class DummyAlgorithm(Algorithm):
    def __init__(self, hash_alg):
        self.hash_alg = hash_alg

    @classmethod
    def from_jwk(cls, *args, **kwargs):
        return cls(None)

    def prepare_key(self, *args, **kwargs):
        return None

    def sign(self, *args, **kwargs):
        raise NotImplementedError

    def verify(self, *args, **kwargs):
        raise NotImplementedError

    def to_jwk(self, *args, **kwargs):
        return {}

def test_compute_hash_digest_raises_when_no_hash_alg():
    alg = DummyAlgorithm(hash_alg=None)
    with pytest.raises(NotImplementedError):
        alg.compute_hash_digest(b"data")

def test_compute_hash_digest_uses_hashlib_when_not_crypto_hash():
    alg = DummyAlgorithm(hash_alg=hashlib.sha256)
    result = alg.compute_hash_digest(b"data")
    assert result == hashlib.sha256(b"data").digest()

def test_compute_hash_digest_uses_cryptography_hash_algorithm_class(monkeypatch):
    monkeypatch.setattr(alg_mod, "has_crypto", True)
    alg = DummyAlgorithm(hash_alg=crypto_hashes.SHA256)

    result = alg.compute_hash_digest(b"hello world")

    digest_expected = crypto_hashes.Hash(crypto_hashes.SHA256(), backend=default_backend())
    digest_expected.update(b"hello world")
    expected = digest_expected.finalize()

    assert result == expected
