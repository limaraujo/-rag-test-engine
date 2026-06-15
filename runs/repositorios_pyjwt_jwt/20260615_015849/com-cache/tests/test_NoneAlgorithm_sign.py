import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm



# Verifica retorno constante para mensagens diversas (happy path)
@pytest.mark.parametrize("msg", [b"", b"data", b"\x00\xff"])
def test_sign_returns_empty_bytes_for_various_messages(msg):
    # cria instância sem chamar __init__ (assumindo classe abstrata)
    instance = object.__new__(NoneAlgorithm)
    assert NoneAlgorithm.sign(instance, msg, None) == b""

# Verifica que sign aceita diferentes valores de key sem erro (caso de borda)
@pytest.mark.parametrize("key", [None, 0, "key", b"bytes"])
def test_sign_accepts_various_keys_without_error(key):
    instance = object.__new__(NoneAlgorithm)
    result = NoneAlgorithm.sign(instance, b"msg", key)
    assert isinstance(result, (bytes,))
    assert result == b""

# Verifica que sign não muta a entrada e retorna bytes (caso de borda)
def test_sign_does_not_mutate_input_message():
    instance = object.__new__(NoneAlgorithm)
    msg = bytearray(b"mutable")
    result = NoneAlgorithm.sign(instance, msg, None)
    assert msg == bytearray(b"mutable")
    assert result == b""
