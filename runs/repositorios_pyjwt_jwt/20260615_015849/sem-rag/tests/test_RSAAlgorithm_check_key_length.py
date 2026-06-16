import pytest
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class _DummyRSAKey:
    def __init__(self, key_size: int):
        self.key_size = key_size

def test_check_key_length_below_min():
    rsa = RSAAlgorithm(hash_alg=hashes.SHA256())
    rsa._MIN_KEY_SIZE = 2048
    key = _DummyRSAKey(1024)
    expected = (
        f"The RSA key is {key.key_size} bits long, which is below "
        f"the minimum recommended size of {rsa._MIN_KEY_SIZE} bits. "
        f"See NIST SP 800-131A."
    )
    assert rsa.check_key_length(key) == expected

@pytest.mark.parametrize("size", [2048, 4096])
def test_check_key_length_none_when_key_size_at_or_above_min(size):
    rsa = RSAAlgorithm(hash_alg=hashes.SHA256())
    rsa._MIN_KEY_SIZE = 2048
    key = _DummyRSAKey(size)
    assert rsa.check_key_length(key) is None
