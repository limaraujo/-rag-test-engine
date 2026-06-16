import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm
import types
import types
import types
import types

import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm


# Test that prepare_key returns the same EC key when given an existing cryptography EC key (happy path)
def test_prepare_key_existing_ec_key_object():
    class Dummy:  # minimal self mock to host required attributes
        pass

    dummy = Dummy()
    dummy._crypto_key_types = (ec.EllipticCurvePublicKey, ec.EllipticCurvePrivateKey)

    def _validate_curve(self_arg, ec_key):
        pass

    import types
    dummy._validate_curve = types.MethodType(_validate_curve, dummy)

    def _check_crypto_key_type(self_arg, key):
        pass

    dummy.check_crypto_key_type = types.MethodType(_check_crypto_key_type, dummy)

    priv_key = ec.generate_private_key(ec.SECP256R1())
    pub_key = priv_key.public_key()

    result = ECAlgorithm.prepare_key(dummy, pub_key)
    assert result is pub_key


# Test that prepare_key loads a PEM-encoded EC public key and returns it
def test_prepare_key_pem_public_key_path():
    class Dummy:  # minimal self mock to host required attributes
        pass

    dummy = Dummy()
    dummy._crypto_key_types = (ec.EllipticCurvePublicKey, ec.EllipticCurvePrivateKey)

    def _validate_curve(self_arg, ec_key):
        pass

    import types
    dummy._validate_curve = types.MethodType(_validate_curve, dummy)

    def _check_crypto_key_type(self_arg, key):
        pass

    dummy.check_crypto_key_type = types.MethodType(_check_crypto_key_type, dummy)

    priv_key = ec.generate_private_key(ec.SECP256R1())
    pub_key = priv_key.public_key()
    pub_pem = pub_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    result = ECAlgorithm.prepare_key(dummy, pub_pem)
    assert isinstance(result, ec.EllipticCurvePublicKey)
    assert result.public_numbers() == pub_key.public_numbers()


# Test that prepare_key raises TypeError on invalid input type (non-key)
def test_prepare_key_invalid_input_type_raises_TypeError():
    class Dummy:
        pass

    dummy = Dummy()
    dummy._crypto_key_types = (ec.EllipticCurvePublicKey, ec.EllipticCurvePrivateKey)

    def _validate_curve(self_arg, ec_key):
        pass

    import types
    dummy._validate_curve = types.MethodType(_validate_curve, dummy)

    def _check_crypto_key_type(self_arg, key):
        pass

    dummy.check_crypto_key_type = types.MethodType(_check_crypto_key_type, dummy)

    with pytest.raises(TypeError):
        ECAlgorithm.prepare_key(dummy, 123)


# Test that prepare_key raises ValueError for invalid PEM content (fallback path raises)
def test_prepare_key_invalid_pem_content_raises_ValueError():
    class Dummy:
        pass

    dummy = Dummy()
    dummy._crypto_key_types = (ec.EllipticCurvePublicKey, ec.EllipticCurvePrivateKey)

    def _validate_curve(self_arg, ec_key):
        pass

    import types
    dummy._validate_curve = types.MethodType(_validate_curve, dummy)

    def _check_crypto_key_type(self_arg, key):
        pass

    dummy.check_crypto_key_type = types.MethodType(_check_crypto_key_type, dummy)

    with pytest.raises(ValueError):
        ECAlgorithm.prepare_key(dummy, b"not-a-pem")
