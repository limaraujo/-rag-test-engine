import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm
# Verifica o verificador retorna False para várias entradas bytes (caminho feliz)

@pytest.mark.parametrize("msg, sig, key", [
    (b"hello", b"sig", None),
    (b"", b"sig", None),
    (b"\x01\x02\x03", b"\x04", None),
    (b"data", b"sig2", None),
    (b"\x00", b"\x01", None),
])
def test_none_algorithm_verify_always_false_happy_path(msg, sig, key):
    algo = NoneAlgorithm()
    assert algo.verify(msg, key, sig) is False

# Verifica comportamento com tipos não-byte para msg/sig (caso de borda)
def test_none_algorithm_verify_with_non_bytes_inputs_returns_false():
    algo = NoneAlgorithm()
    assert algo.verify("not bytes", "not bytes", None) is False

# Verifica que o parâmetro key não-None é ignorado pelo verificador (caso de borda)
def test_none_algorithm_verify_ignores_non_none_key_returns_false():
    algo = NoneAlgorithm()
    assert algo.verify(b"msg", key=123, sig=b"sig") is False
