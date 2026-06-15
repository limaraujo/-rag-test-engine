import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey, EllipticCurvePrivateKey
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# Dummy self to simulate ECAlgorithm instance surface required by prepare_key
class DummySelf:
    def __init__(self):
        self._crypto_key_types = (EllipticCurvePublicKey, EllipticCurvePrivateKey)

    def _validate_curve(self, key):
        pass

    def check_crypto_key_type(self, key):
        pass

# Verifica caminho quando chave já é tipo criptográfico (branch de chave já carregada)
def test_prepare_key_with_existing_ec_key_branch_A():
    dummy = DummySelf()
    priv = ec.generate_private_key(ec.SECP256R1(), default_backend())
    result = ECAlgorithm.prepare_key(dummy, priv)
    assert result is priv

# Verifica caminho com PEM pública (public key em PEM)
def test_prepare_key_with_public_pem_returns_public_key():
    dummy = DummySelf()
    # Gerar uma chave privada para obter a chave pública
    priv = ec.generate_private_key(ec.SECP256R1(), default_backend())
    pub = priv.public_key()
    pem_public = pub.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    result = ECAlgorithm.prepare_key(dummy, pem_public)
    assert isinstance(result, EllipticCurvePublicKey)

# Verifica caminho com PEM privada (fallback após falha de PEM pública)
def test_prepare_key_with_private_pem_fallback_returns_private_key():
    dummy = DummySelf()
    priv = ec.generate_private_key(ec.SECP256R1(), default_backend())
    pem_private = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    result = ECAlgorithm.prepare_key(dummy, pem_private)
    assert isinstance(result, EllipticCurvePrivateKey)

# Verifica exceção para input inválido (TypeError)
def test_prepare_key_invalid_input_raises_typeerror():
    dummy = DummySelf()
    with pytest.raises(TypeError):
        ECAlgorithm.prepare_key(dummy, 123)
