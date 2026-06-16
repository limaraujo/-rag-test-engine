from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


class _DummyHMAC(HMACAlgorithm):
    def __init__(self):
        pass

    def sign(self, msg: bytes, key: bytes) -> bytes:
        return b"fixed-signature"


# Verifica caminho feliz: sig igual ao resultado de sign(msg, key)
def test_hmac_verify_happy_path():
    alg = _DummyHMAC()
    msg = b"hello"
    key = b"secret"
    expected = alg.sign(msg, key)
    assert alg.verify(msg, key, expected) is True


# Verifica falha quando sig difere do resultado de sign(msg, key)
def test_hmac_verify_false_on_wrong_signature():
    alg = _DummyHMAC()
    msg = b"hello"
    key = b"secret"
    wrong = b"not-the-signature"
    assert alg.verify(msg, key, wrong) is False
