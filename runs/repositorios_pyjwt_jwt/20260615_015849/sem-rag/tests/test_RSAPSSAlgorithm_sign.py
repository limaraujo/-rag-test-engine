import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm

# Dummy key to capture inputs to sign
class DummyKey:
    def __init__(self, should_raise: bool = False):
        self.should_raise = should_raise
        self.called = False
        self.args = None

    def sign(self, data, pad, algorithm):
        self.called = True
        self.args = (data, pad, algorithm)
        if self.should_raise:
            raise ValueError("boom")
        return b"signature"

# Test: happy path with different hash algorithms, verifying internal padding configuration
@pytest.mark.parametrize("hash_alg_class", [hashes.SHA256, hashes.SHA384])
def test_sign_uses_pss_with_expected_parameters(hash_alg_class):
    # Create instance without calling __init__ to avoid constructor requirements
    alg = RSAPSSAlgorithm.__new__(RSAPSSAlgorithm)
    alg.hash_alg = lambda: hash_alg_class()

    key = DummyKey()
    msg = b"hello"

    signature = alg.sign(msg, key)

    assert signature == b"signature"
    assert key.called
    data, pad, algorithm = key.args
    assert data == msg
    assert isinstance(algorithm, hash_alg_class)
    assert isinstance(pad, padding.PSS)
    assert isinstance(pad.mgf, padding.MGF1)

    # Access salt_length in a way that's robust to different versions of cryptography
    salt_length = getattr(pad, "salt_length", None)
    if salt_length is None:
        salt_length = getattr(pad, "_salt_length", None)
    assert salt_length == hash_alg_class().digest_size

# Test: exception raised by the key-signing process is propagated
def test_sign_propagates_exception_from_key():
    alg = RSAPSSAlgorithm.__new__(RSAPSSAlgorithm)
    alg.hash_alg = lambda: hashes.SHA256()

    key = DummyKey(should_raise=True)
    msg = b"data"

    with pytest.raises(ValueError, match="boom"):
        alg.sign(msg, key)
