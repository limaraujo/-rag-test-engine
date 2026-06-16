import pytest
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

class _DummyKey:
    def sign(self, data: bytes) -> bytes:
        return b"EDDSA:" + data

@pytest.mark.parametrize("msg, expected", [
    ("hello", b"EDDSA:hello"),
    (b"world", b"EDDSA:world"),
])
def test_okp_algorithm_sign_accepts_str_and_bytes(msg, expected):
    # Verifica sign com msg como str ou bytes (caminho feliz)
    algo = OKPAlgorithm()
    key = _DummyKey()
    assert algo.sign(msg, key) == expected
