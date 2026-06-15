import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# curto: verifica caminho feliz do método verify retorna False
def test_none_algorithm_verify_basic_false():
    alg = NoneAlgorithm()
    assert alg.verify(b"hello", None, b"signature") is False

# curto: cobre cenários variados com parâmetros
@pytest.mark.parametrize("msg,sig", [
    (b"", b""),
    (b"data", b"sig"),
    (b"another data", b"")
])
def test_none_algorithm_verify_various_inputs_always_false(msg, sig):
    alg = NoneAlgorithm()
    assert alg.verify(msg, None, sig) is False

# curto: verifica que chave fornecida é ignorada e ainda retorna False
def test_none_algorithm_verify_ignores_key_and_returns_false():
    alg = NoneAlgorithm()
    assert alg.verify(b"msg", object(), b"sig") is False
