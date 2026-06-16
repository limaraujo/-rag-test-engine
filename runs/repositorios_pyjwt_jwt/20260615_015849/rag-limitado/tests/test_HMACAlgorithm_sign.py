import hmac
import hashlib
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# curto: caminho feliz - sha256, compara com hmac padrão
def test_sign_matches_hmac_sha256_happy_path():
    algo = HMACAlgorithm(hashlib.sha256)
    key = b"secret"
    msg = b"hello"
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert algo.sign(msg, key) == expected

# curto: compara sha256 vs sha1 para o mesmo input/key; verifica diferenças e correspondências esperadas
def test_sign_diff_hash_algorithms_produce_different_results():
    algo_sha256 = HMACAlgorithm(hashlib.sha256)
    algo_sha1 = HMACAlgorithm(hashlib.sha1)
    key = b"secret"
    msg = b"hey"
    res256 = algo_sha256.sign(msg, key)
    res1 = algo_sha1.sign(msg, key)
    assert res256 != res1
    assert res256 == hmac.new(key, msg, hashlib.sha256).digest()
    assert res1 == hmac.new(key, msg, hashlib.sha1).digest()

# curto: borda - entradas vazias
def test_sign_with_empty_inputs():
    algo = HMACAlgorithm(hashlib.sha256)
    key = b""
    msg = b""
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert algo.sign(msg, key) == expected

# curto: caso de borda com dados grandes
def test_sign_with_large_message():
    algo = HMACAlgorithm(hashlib.sha256)
    key = b"aaa" * 1000
    msg = b"bbb" * 1000
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert algo.sign(msg, key) == expected
