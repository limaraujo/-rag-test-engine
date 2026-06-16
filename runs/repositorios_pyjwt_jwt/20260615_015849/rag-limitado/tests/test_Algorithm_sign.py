import pytest
import hmac
import hashlib
from repositorios.pyjwt.jwt.algorithms import Algorithm

class DummyAlgorithm(Algorithm):
    def sign(self, msg: bytes, key: bytes) -> bytes:
        return hmac.new(key, msg, hashlib.sha256).digest()

    @classmethod
    def from_jwk(cls, jwk):
        return cls()

    def prepare_key(self, key):
        return key

    def to_jwk(self):
        return {}

    def verify(self, msg: bytes, signature: bytes, key: bytes) -> bool:
        expected = hmac.new(key, msg, hashlib.sha256).digest()
        return expected == signature

# happy path: signature matches HMAC-SHA256 for given messages and a fixed key
@pytest.mark.parametrize("msg", [b"hello", b"world"])
def test_sign_happy_path(msg):
    alg = DummyAlgorithm()
    key = b"secret"
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert alg.sign(msg, key) == expected

# edge case: empty message should still produce a valid signature
def test_sign_empty_message():
    alg = DummyAlgorithm()
    msg = b""
    key = b"secret"
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert alg.sign(msg, key) == expected

# exception path: non-bytes key should raise a TypeError
def test_sign_invalid_key_type_raises_type_error():
    alg = DummyAlgorithm()
    msg = b"data"
    key = "notbytes"  # invalid type
    with pytest.raises(TypeError):
        alg.sign(msg, key)

# branching: same message with different keys should yield different signatures
def test_sign_different_keys_produce_different_signatures():
    alg = DummyAlgorithm()
    msg = b"same message"
    key1 = b"secret1"
    key2 = b"secret2"
    sig1 = alg.sign(msg, key1)
    sig2 = alg.sign(msg, key2)
    assert sig1 != sig2
