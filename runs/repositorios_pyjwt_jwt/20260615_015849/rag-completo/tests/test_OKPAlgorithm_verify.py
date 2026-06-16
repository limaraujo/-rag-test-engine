import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# Teste de caminho feliz: usa chave privada Ed25519 e mensagem string
def test_verify_happy_path_with_private_key_string():
    private_key = Ed25519PrivateKey.generate()
    message = "hello world"
    signature = private_key.sign(message.encode("utf-8"))

    algo = OKPAlgorithm()
    assert algo.verify(message, private_key, signature) is True

# Teste de caminho feliz: usa chave pública Ed25519 com assinatura válida
def test_verify_happy_path_with_public_key_string():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    message = "hello world"
    signature = private_key.sign(message.encode("utf-8"))

    algo = OKPAlgorithm()
    assert algo.verify(message, public_key, signature) is True

# Teste de falha: assinatura inválida deve retornar False
def test_verify_invalid_signature_returns_false():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    message = "tampered message"
    signature = private_key.sign(message.encode("utf-8"))

    # altera o signature para simular corrupção
    bad_signature = bytearray(signature)
    if len(bad_signature) > 0:
        bad_signature[0] ^= 0x01
    algo = OKPAlgorithm()
    assert algo.verify(message, public_key, bytes(bad_signature)) is False

# Teste de cobertura: msg como str/bytes e chave privada/public
@pytest.mark.parametrize("msg_type", ["string", "bytes"])
@pytest.mark.parametrize("key_variant", ["private", "public"])
def test_verify_handles_string_and_bytes_msg_and_key_variants(msg_type, key_variant):
    private_key = Ed25519PrivateKey.generate()
    msg_for_sign = "hello" if msg_type == "string" else b"hello"
    sign_input = msg_for_sign.encode("utf-8") if isinstance(msg_for_sign, str) else msg_for_sign
    signature = private_key.sign(sign_input)

    key = private_key if key_variant == "private" else private_key.public_key()
    verify_input = "hello" if msg_type == "string" else b"hello"

    algo = OKPAlgorithm()
    assert algo.verify(verify_input, key, signature) is True
