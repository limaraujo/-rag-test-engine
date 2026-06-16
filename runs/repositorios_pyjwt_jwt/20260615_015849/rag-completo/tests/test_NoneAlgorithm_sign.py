import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm


# curto: happy path com várias mensagens; garante assinatura vazia
@pytest.mark.parametrize("msg", [b"hello", b"", b"world", b"12345"])
def test_sign_returns_empty_bytes_happy_path(msg):
    algo = NoneAlgorithm()
    assert algo.sign(msg, None) == b""

# curto: tipo de retorno é bytes
def test_sign_return_type_is_bytes():
    algo = NoneAlgorithm()
    result = algo.sign(b"test", None)
    assert isinstance(result, bytes)

# curto: consistência com entradas diferentes; assinatura permanece vazia
def test_sign_consistent_empty_signature_across_inputs():
    algo = NoneAlgorithm()
    assert algo.sign(b"a", None) == b""
    assert algo.sign(b"b", None) == b""
