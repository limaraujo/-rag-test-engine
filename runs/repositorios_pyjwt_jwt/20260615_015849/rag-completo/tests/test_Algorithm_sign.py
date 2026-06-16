import pytest
from typing import Any
from repositorios.pyjwt.jwt.algorithms import Algorithm

class DummyAlgorithm(Algorithm):
    @classmethod
    def from_jwk(cls, jwk: dict) -> "Algorithm":
        return cls()

    def prepare_key(self, key: Any) -> Any:
        return key

    def to_jwk(self) -> dict:
        return {}

    def verify(self, msg: bytes, sig: bytes, key: Any) -> None:
        return None

    def sign(self, msg: bytes, key: Any) -> bytes:
        key_bytes = (
            key.encode() if isinstance(key, str) else
            key if isinstance(key, (bytes, bytearray)) else
            str(key).encode()
        )
        return b"dummy-sign:" + key_bytes + b":" + msg

def test_abstract_algorithm_sign_is_abstract():
    with pytest.raises(TypeError):
        Algorithm()

@pytest.mark.parametrize("key,msg,expected", [
    ("mykey", b"hello", b"dummy-sign:mykey:hello"),
    (123, b"hello", b"dummy-sign:123:hello"),
])
def test_concrete_algorithm_sign_implements_and_works(key, msg, expected):
    alg = DummyAlgorithm()
    assert alg.sign(msg, key) == expected
