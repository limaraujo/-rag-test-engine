import hashlib
import hmac
import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# verifica assinatura com SHA256 no caminho feliz
def test_sign_happy_path_sha256():
    key = b"secret_key"
    msg = b"The quick brown fox"
    algo = HMACAlgorithm(hash_alg=hashlib.sha256)
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert algo.sign(msg, key) == expected

# verifica que o sign usa o digestmod correto para diferentes hash_alg
@pytest.mark.parametrize("hash_alg", [hashlib.sha1, hashlib.sha256, hashlib.sha512])
def test_sign_matches_various_hash_algorithms(hash_alg):
    key = b"k"
    msg = b"message"
    algo = HMACAlgorithm(hash_alg=hash_alg)
    expected = hmac.new(key, msg, hash_alg).digest()
    assert algo.sign(msg, key) == expected

# verifica que inputs não são modificados pela assinatura
def test_sign_no_input_mutation():
    key = b"abc"
    msg = b"def"
    algo = HMACAlgorithm(hash_alg=hashlib.sha256)
    key_before = key[:]
    msg_before = msg[:]
    algo.sign(msg, key)
    assert key == key_before
    assert msg == msg_before
