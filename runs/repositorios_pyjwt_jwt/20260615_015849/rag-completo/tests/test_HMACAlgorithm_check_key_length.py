import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# Verifica retorno quando a chave é menor que o mínimo recomendado (caso de borda)
class _TestHMACBelowMin(HMACAlgorithm):
    def __init__(self):
        pass
    def hash_alg(self):
        class _FakeAlg:
            digest_size = 32
            name = "sha256"
        return _FakeAlg()

def test_check_key_length_below_min():
    h = _TestHMACBelowMin()
    key = b""
    expected = (
        "The HMAC key is 0 bytes long, which is below "
        "the minimum recommended length of 32 bytes for "
        "SHA256. "
        "See RFC 7518 Section 3.2."
    )
    assert h.check_key_length(key) == expected

# Verifica None (happy path) quando o tamanho da chave atende ou excede o mínimo
@pytest.mark.parametrize("length", [32, 64])
def test_check_key_length_ok(length):
    class _TestHMACOk(HMACAlgorithm):
        def __init__(self):
            pass
        def hash_alg(self):
            class _FakeAlg:
                digest_size = 32
                name = "sha256"
            return _FakeAlg()
    h = _TestHMACOk()
    key = b"a" * length
    assert h.check_key_length(key) is None
