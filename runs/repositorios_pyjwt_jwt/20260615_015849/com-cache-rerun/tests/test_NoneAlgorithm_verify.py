import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm


# Verifica que NoneAlgorithm.verify retorna False para entradas variadas (caminho feliz)
@pytest.mark.parametrize("msg,sig", [
    (b"", b""),
    (b"hello", b"sig"),
    (b"123456", b"\x00\x01\x02"),
    (b"\xff" * 32, b"\xaa" * 64),
])
def test_none_algorithm_verify_always_false_various(msg, sig):
    alg = NoneAlgorithm()
    assert alg.verify(msg, None, sig) is False

# Verifica que NoneAlgorithm.verify retorna False para entradas muito grandes (caso de borda)
def test_none_algorithm_verify_large_inputs_always_false():
    large_msg = b"a" * 10000
    large_sig = b"b" * 20000
    alg = NoneAlgorithm()
    assert alg.verify(large_msg, None, large_sig) is False
