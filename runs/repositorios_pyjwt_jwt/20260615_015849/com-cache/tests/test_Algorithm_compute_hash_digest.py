import hashlib
import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import repositorios.pyjwt.jwt.algorithms as alg_mod
from repositorios.pyjwt.jwt.algorithms import Algorithm

@pytest.fixture(autouse=True)
def allow_instantiation_of_algorithm():
    # Allow instantiation of abstract Algorithm for tests by bypassing ABC checks
    orig = getattr(alg_mod.Algorithm, "__abstractmethods__", frozenset())
    alg_mod.Algorithm.__abstractmethods__ = frozenset()
    if not hasattr(alg_mod, "has_crypto"):
        setattr(alg_mod, "has_crypto", True)
    try:
        yield
    finally:
        alg_mod.Algorithm.__abstractmethods__ = orig


def test_compute_hash_digest_with_sha256_hash_algorithm_class(monkeypatch):
    monkeypatch.setattr(alg_mod, "has_crypto", True, raising=False)
    inst = alg_mod.Algorithm.__new__(alg_mod.Algorithm)
    inst.hash_alg = hashes.SHA256
    data = b"hello world"
    expected = hashes.Hash(hashes.SHA256(), backend=default_backend())
    expected.update(data)
    expected_digest = expected.finalize()
    assert inst.compute_hash_digest(data) == expected_digest


def test_compute_hash_digest_with_hashlib_callable():
    inst = alg_mod.Algorithm.__new__(alg_mod.Algorithm)
    inst.hash_alg = hashlib.sha256
    data = b"abc"
    assert inst.compute_hash_digest(data) == hashlib.sha256(data).digest()


def test_compute_hash_digest_raises_not_implemented_when_no_hash_alg():
    inst = alg_mod.Algorithm.__new__(alg_mod.Algorithm)
    with pytest.raises(NotImplementedError):
        inst.compute_hash_digest(b"data")
