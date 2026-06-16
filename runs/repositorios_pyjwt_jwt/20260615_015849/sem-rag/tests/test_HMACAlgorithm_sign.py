import hashlib
import hmac
import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# Verifica assinatura com SHA-256 no caminho feliz
def test_sign_sha256_happy_path():
    key = b"secret-key"
    msg = b"the quick brown fox"
    algo = HMACAlgorithm(hashlib.sha256)
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert algo.sign(msg, key) == expected

# Verifica que sign usa o digest correspondente para SHA-256 e SHA-384
@pytest.mark.parametrize("hash_alg", [hashlib.sha256, hashlib.sha384])
def test_sign_matches_expected_for_multiple_hash_algorithms(hash_alg):
    key = b"secret"
    msg = b"hello world"
    algo = HMACAlgorithm(hash_alg)
    expected = hmac.new(key, msg, hash_alg).digest()
    assert algo.sign(msg, key) == expected

# Verifica comportamento com msg e key vazios
def test_sign_with_empty_inputs():
    key = b""
    msg = b""
    algo = HMACAlgorithm(hashlib.sha256)
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert algo.sign(msg, key) == expected

# Verifica tamanho do digest correspondente ao algoritmo
@pytest.mark.parametrize("hash_alg, expected_size", [
    (hashlib.sha256, 32),
    (hashlib.sha384, 48),
    (hashlib.sha512, 64),
])
def test_sign_digest_size_matches_expected(hash_alg, expected_size):
    algo = HMACAlgorithm(hash_alg)
    res = algo.sign(b"data", b"key")
    assert len(res) == expected_size
