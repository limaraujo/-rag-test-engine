import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# happy path: test OKPAlgorithm.sign for Ed25519 and Ed448 with both string and bytes inputs
@pytest.mark.parametrize("key_type,msg", [
    ("ed25519", "hello"),
    ("ed25519", b"hello"),
    ("ed448", "hello"),
    ("ed448", b"hello"),
])
def test_okp_algorithm_sign_parametrized(key_type, msg):
    if key_type == "ed25519":
        key = Ed25519PrivateKey.generate()
    else:
        key = Ed448PrivateKey.generate()

    alg = OKPAlgorithm()
    expected_input = msg if isinstance(msg, (bytes, bytearray)) else str(msg).encode("utf-8")
    expected = key.sign(expected_input)
    signature = alg.sign(msg, key)
    assert signature == expected
