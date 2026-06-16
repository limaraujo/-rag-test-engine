import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# curto: happy path com Ed25519 usando string e bytes
def test_okp_sign_ed25519_happy_path():
    key = Ed25519PrivateKey.generate()
    algo = OKPAlgorithm()
    msg_str = "hello"
    sig_from_str = algo.sign(msg_str, key)
    expected_str = key.sign(msg_str.encode("utf-8"))
    assert sig_from_str == expected_str

    msg_bytes = b"hello"
    sig_from_bytes = algo.sign(msg_bytes, key)
    expected_bytes = key.sign(msg_bytes)
    assert sig_from_bytes == expected_bytes

# curto: happy path com Ed448 usando string e bytes
def test_okp_sign_ed448_happy_path():
    key = Ed448PrivateKey.generate()
    algo = OKPAlgorithm()
    msg_str = "hello"
    sig_from_str = algo.sign(msg_str, key)
    expected_str = key.sign(msg_str.encode("utf-8"))
    assert sig_from_str == expected_str

    msg_bytes = b"hello"
    sig_from_bytes = algo.sign(msg_bytes, key)
    expected_bytes = key.sign(msg_bytes)
    assert sig_from_bytes == expected_bytes

# curto: caminho de erro: chave inválida (sem método sign) deve levantar AttributeError
def test_okp_sign_invalid_key_raises_attribute_error():
    class DummyKey:
        pass

    algo = OKPAlgorithm()
    with pytest.raises(AttributeError):
        algo.sign("message", DummyKey())
