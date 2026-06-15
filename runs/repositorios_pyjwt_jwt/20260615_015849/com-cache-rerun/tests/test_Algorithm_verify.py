import pytest
from typing import Any
from repositorios.pyjwt.jwt.algorithms import Algorithm

class DummyAlgorithm(Algorithm):
    @classmethod
    def from_jwk(cls, jwk: Any) -> "Algorithm":
        return cls()

    def prepare_key(self, key: Any) -> Any:
        return key

    def sign(self, msg: bytes, key: Any) -> bytes:
        return b""

    def to_jwk(self) -> dict:
        return {}

    def verify(self, msg: bytes, key: Any, sig: bytes) -> bool:
        expected = b"valid:" + msg
        return sig == expected

# Verifica que não é possível instanciar a classe base abstrata Algorithm (verify abstract)
def test_base_algorithm_is_abstract():
    with pytest.raises(TypeError):
        Algorithm()

# happy path: assinatura correta é reconhecida
def test_verify_matches_signature():
    algo = DummyAlgorithm()
    msg = b"message"
    sig = b"valid:" + msg
    assert algo.verify(msg, None, sig) is True

# branch/edge: assinatura incorreta deve falhar
def test_verify_mismatch_signature():
    algo = DummyAlgorithm()
    msg = b"message"
    sig = b"invalid"
    assert algo.verify(msg, None, sig) is False

# borda: mensagem vazia deve ainda funcionar com assinatura esperada
def test_verify_with_empty_message():
    algo = DummyAlgorithm()
    msg = b""
    sig = b"valid:" + msg
    assert algo.verify(msg, None, sig) is True
