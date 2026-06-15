import importlib
import hashlib
import pytest
from types import SimpleNamespace
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from repositorios.pyjwt.jwt.algorithms import Algorithm

ALG_MODULE = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
Algorithm = ALG_MODULE.Algorithm

# verificar branch usando um type subclass de HashAlgorithm (cryptography)
def test_compute_hash_digest_type_hash_algorithm_branch():
    ALG_MODULE.has_crypto = True
    data = b"hello world"
    dummy_self = SimpleNamespace(hash_alg=hashes.SHA256)
    result = Algorithm.compute_hash_digest(dummy_self, data)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data)
    expected = digest.finalize()
    assert result == expected

# verificar branch else com hash_alg como callable (hashlib.sha256)
def test_compute_hash_digest_callable_branch():
    ALG_MODULE.has_crypto = True
    data = b"another message"
    dummy_self = SimpleNamespace(hash_alg=hashlib.sha256)
    result = Algorithm.compute_hash_digest(dummy_self, data)
    expected = hashlib.sha256(data).digest()
    assert result == expected

# verificar NotImplementedError quando hash_alg é None
def test_compute_hash_digest_raises_when_hash_alg_missing():
    ALG_MODULE.has_crypto = True
    dummy_self = SimpleNamespace(hash_alg=None)
    with pytest.raises(NotImplementedError):
        Algorithm.compute_hash_digest(dummy_self, b"data")
