import types
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

def _make_algo_with_fake_sign(sign_func):
    obj = object.__new__(HMACAlgorithm)
    obj.sign = types.MethodType(sign_func, obj)
    return obj

# curto: happy path - sig == sign(msg, key) => verify returns True
def test_verify_hmac_algorithm_happy_path():
    def fake_sign(self, msg, key):
        return b"expected_signature"
    algo = _make_algo_with_fake_sign(fake_sign)
    msg = b"hello"
    key = b"secret"
    sig = b"expected_signature"
    assert algo.verify(msg, key, sig) is True

# curto: mismatch - sig != sign(msg, key) => verify returns False
def test_verify_hmac_algorithm_signature_mismatch():
    def fake_sign(self, msg, key):
        return b"expected_signature"
    algo = _make_algo_with_fake_sign(fake_sign)
    msg = b"hello"
    key = b"secret"
    sig = b"different_signature"
    assert algo.verify(msg, key, sig) is False
