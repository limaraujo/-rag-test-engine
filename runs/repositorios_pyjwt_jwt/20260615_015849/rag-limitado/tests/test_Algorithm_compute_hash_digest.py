import hashlib
import pytest
from cryptography.hazmat.primitives import hashes
import repositorios.pyjwt.jwt.algorithms as alg_module
from repositorios.pyjwt.jwt.algorithms import Algorithm

# Ensure the module uses the cryptography backend when needed
alg_module.has_crypto = True

# NotImplemented path: missing hash_alg attribute
def test_compute_hash_digest_raises_without_hash_alg():
    # NotImplemented path: no hash_alg defined on the receiver
    class Obj: pass
    o = Obj()
    with pytest.raises(NotImplementedError):
        Algorithm.compute_hash_digest(o, b"data")

# Cryptography path: hash_alg is a cryptography HashAlgorithm subclass
def test_compute_hash_digest_cryptography_path():
    # Happy path: cryptography path with SHA256
    o = type("O", (), {})()
    o.hash_alg = hashes.SHA256
    data = b"abc"
    expected = hashlib.sha256(data).digest()
    result = Algorithm.compute_hash_digest(o, data)
    assert result == expected

# Fallback path: hash_alg is a Python hashlib constructor
def test_compute_hash_digest_hashlib_path():
    # Fallback path: hashlib.sha256 (callable) used instead of cryptography path
    o = type("O2", (), {})()
    o.hash_alg = hashlib.sha256
    data = b"xyz"
    expected = hashlib.sha256(data).digest()
    result = Algorithm.compute_hash_digest(o, data)
    assert result == expected

# Edge case: empty input with cryptography path
def test_compute_hash_digest_empty_input_cryptography_path():
    o = type("O3", (), {})()
    o.hash_alg = hashes.SHA256
    data = b""
    expected = hashlib.sha256(data).digest()
    result = Algorithm.compute_hash_digest(o, data)
    assert result == expected
