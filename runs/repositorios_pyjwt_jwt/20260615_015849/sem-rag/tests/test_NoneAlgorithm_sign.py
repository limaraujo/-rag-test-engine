import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# curto: verifica/sign retorna bytes vazios para inputs variados (caminho feliz)
@pytest.mark.parametrize("msg", [
    b"",
    b"hello",
    b"\x00\x01\x02"
])
def test_none_algorithm_sign_happy_path_returns_empty_bytes(msg):
    algo = NoneAlgorithm()
    assert algo.sign(msg, None) == b""

# curto: verifica o tipo de retorno é bytes e o comprimento é zero
def test_none_algorithm_sign_returns_empty_bytes_type_and_zero_length():
    algo = NoneAlgorithm()
    res = algo.sign(b"data", None)
    assert isinstance(res, bytes)
    assert len(res) == 0
