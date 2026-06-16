import hmac
import hashlib
import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# Verifica que sign usa o hash correto para diferentes hash_alg (casos happy path)
@pytest.mark.parametrize("hash_alg, msg, key", [
    (hashlib.sha256, b"hello", b"secret"),
    (hashlib.sha512, b"world", b"another_key"),
    (hashlib.sha1, b"", b"empty_msg_key"),
])
def test_hmac_algorithm_sign_matches_builtin(hash_alg, msg, key):
    mac = HMACAlgorithm(hash_alg)
    assert mac.sign(msg, key) == hmac.new(key, msg, hash_alg).digest()
