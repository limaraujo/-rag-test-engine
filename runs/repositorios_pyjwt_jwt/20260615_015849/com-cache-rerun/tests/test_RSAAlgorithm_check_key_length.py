import pytest
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

def test_check_key_length_below_minimum_returns_error():
    algo = RSAAlgorithm(hashes.SHA256())
    min_size = algo._MIN_KEY_SIZE

    class DummyKey:
        def __init__(self, size):
            self.key_size = size

    key = DummyKey(min_size - 1)
    expected = (
        f"The RSA key is {key.key_size} bits long, which is below "
        f"the minimum recommended size of {min_size} bits. "
        f"See NIST SP 800-131A."
    )

    assert algo.check_key_length(key) == expected

def test_check_key_length_at_or_above_minimum_returns_none():
    algo = RSAAlgorithm(hashes.SHA256())
    min_size = algo._MIN_KEY_SIZE

    class DummyKey:
        def __init__(self, size):
            self.key_size = size

    key = DummyKey(min_size)
    assert algo.check_key_length(key) is None
