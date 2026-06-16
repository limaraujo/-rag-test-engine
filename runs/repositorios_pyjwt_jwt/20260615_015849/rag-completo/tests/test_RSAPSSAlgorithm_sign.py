import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm
from cryptography.hazmat.primitives.asymmetric import padding as _padding

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm


# Dummy RSA private key to capture the inputs passed to sign()
class DummyRSAPrivateKey:
    def __init__(self, result: bytes = b"signature"):
        self.result = result
        self.calls = []

    def sign(self, msg, pad, alg):
        self.calls.append((msg, pad, alg))
        return self.result


# Subclass of RSAPSSAlgorithm to control hash_alg() used by sign()
class TestRSAPSSAlgorithm(RSAPSSAlgorithm):
    def __init__(self, hash_alg_instance):
        self._hash_alg = hash_alg_instance

    def hash_alg(self):
        return self._hash_alg


def _salt_length(pad):
    # Some versions of cryptography expose salt_length as a public attribute,
    # others expose it as a private _salt_length. Support both.
    if hasattr(pad, "salt_length"):
        return pad.salt_length
    return getattr(pad, "_salt_length")


# Test 1: happy path - verify correct padding type, hash usage, salt length, and returned signature
def test_sign_basic_happy_path():
    algo = TestRSAPSSAlgorithm(hashes.SHA256())
    key = DummyRSAPrivateKey(result=b"signature-by-key")

    signature = algo.sign(b"message", key)

    assert signature == b"signature-by-key"
    assert len(key.calls) == 1

    msg, pad, alg = key.calls[0]
    from cryptography.hazmat.primitives.asymmetric import padding as _padding

    assert msg == b"message"
    assert isinstance(pad, _padding.PSS)
    # hash_alg() should be used for the digest algorithm both in PSS and as the signing digest
    assert alg is algo.hash_alg()
    assert _salt_length(pad) == algo.hash_alg().digest_size


# Test 2: parameterized check that salt_length equals the digest_size of the chosen hash algorithm
@pytest.mark.parametrize("hash_algo_class, expected_digest_size", [
    (hashes.SHA256, 32),
    (hashes.SHA1, 20),
])
def test_sign_salt_length_matches_digest_size(hash_algo_class, expected_digest_size):
    algo = TestRSAPSSAlgorithm(hash_algo_class())
    key = DummyRSAPrivateKey(result=b"sig")

    algo.sign(b"m", key)

    _, pad, alg = key.calls[0]
    assert _salt_length(pad) == alg.digest_size == expected_digest_size


# Test 3: exception propagation - if key.sign raises, sign() should propagate the exception
def test_sign_propagates_exceptions():
    class BadKey(DummyRSAPrivateKey):
        def sign(self, *args, **kwargs):
            raise ValueError("bad key")

    algo = TestRSAPSSAlgorithm(hashes.SHA256())
    bad_key = BadKey()

    with pytest.raises(ValueError, match="bad key"):
        algo.sign(b"data", bad_key)
