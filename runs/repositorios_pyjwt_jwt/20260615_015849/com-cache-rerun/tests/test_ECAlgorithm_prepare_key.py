import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey, EllipticCurvePrivateKey
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm



class DummyEC(ECAlgorithm):
    def __init__(self):
        self._crypto_key_types = (EllipticCurvePublicKey, EllipticCurvePrivateKey)

    def _validate_curve(self, key):
        pass

    def check_crypto_key_type(self, key):
        pass


# happy path: chave já é um objeto EC e deve ser retornada sem alteração
def test_prepare_key_existing_ec_key_instance():
    priv = ec.generate_private_key(ec.SECP256R1())
    dummy = DummyEC()
    result = dummy.prepare_key(priv)
    assert result is priv


# path pública PEM: carrega uma chave pública a partir de PEM e retorna EC public key
def test_prepare_key_public_pem_loading():
    priv = ec.generate_private_key(ec.SECP256R1())
    pub = priv.public_key()
    pem_public = pub.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    dummy = DummyEC()
    result = dummy.prepare_key(pem_public)

    assert isinstance(result, EllipticCurvePublicKey)
    assert result.public_numbers() == pub.public_numbers()


# path PEM privada: PEM de chave privada deve retornar EC private key
def test_prepare_key_private_pem_loading():
    priv = ec.generate_private_key(ec.SECP256R1())
    priv_pem = priv.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption())

    dummy = DummyEC()
    result = dummy.prepare_key(priv_pem)

    assert isinstance(result, EllipticCurvePrivateKey)
    assert result.private_numbers() == priv.private_numbers()


# invalid input type: deve levantar TypeError
def test_prepare_key_invalid_input_type_raises_type_error():
    dummy = DummyEC()
    with pytest.raises(TypeError):
        dummy.prepare_key(123)
