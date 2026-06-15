import hashlib
import hmac
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


# verifica que sign encaminha key, msg e hash_alg para hmac.new e retorna digest
def test_sign_passes_input_and_hash_alg(monkeypatch):
    captured = {}
    class DummyDigest:
        def __init__(self, key, msg, digestmod):
            captured['args'] = (key, msg, digestmod)
        def digest(self):
            return b"FAKE_DIGEST"
    def fake_new(key, msg, digestmod):
        return DummyDigest(key, msg, digestmod)
    monkeypatch.setattr("repositorios.pyjwt.jwt.algorithms.hmac.new", fake_new)
    alg = HMACAlgorithm(hash_alg="MOCK_HASH")
    result = alg.sign(b"m", b"k")
    assert result == b"FAKE_DIGEST"
    assert captured['args'] == (b"k", b"m", "MOCK_HASH")

# verifica que sign produz o mesmo resultado que hmac.new com hashlib.sha256
def test_sign_matches_python_hmac_with_sha256():
    alg = HMACAlgorithm(hash_alg=hashlib.sha256)
    msg = b"hello"
    key = b"secret"
    expected = hmac.new(key, msg, hashlib.sha256).digest()
    assert alg.sign(msg, key) == expected
