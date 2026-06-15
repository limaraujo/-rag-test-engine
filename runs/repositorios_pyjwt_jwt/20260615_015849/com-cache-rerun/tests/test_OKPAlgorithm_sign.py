import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# Verifica assinatura correta com msg em str/bytes usando Ed25519/Ed448 (caminho feliz)
@pytest.mark.parametrize("key_class, msg", [
    (Ed25519PrivateKey, "hello"),
    (Ed25519PrivateKey, b"hello"),
    (Ed448PrivateKey, "hello"),
    (Ed448PrivateKey, b"hello"),
])
def test_okp_algorithm_sign_happy_path(key_class, msg):
    key = key_class.generate()
    alg = OKPAlgorithm()
    to_bytes = lambda m: m.encode("utf-8") if isinstance(m, str) else m
    expected = key.sign(to_bytes(msg))
    result = alg.sign(msg, key)
    assert result == expected
