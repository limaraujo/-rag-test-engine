import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# Verifica o caminho feliz usando um dict de JWK
def test_from_jwk_happy_path_dict():
    jwk = {"kty": "oct", "k": "c2VjcmV0"}  # base64url de b"secret"
    assert HMACAlgorithm.from_jwk(jwk) == b"secret"

# Verifica o caminho feliz usando uma string JSON de JWK
def test_from_jwk_happy_path_str():
    jwk = '{"kty":"oct","k":"c2VjcmV0"}'
    assert HMACAlgorithm.from_jwk(jwk) == b"secret"

# Verifica exceção quando kty não é oct
def test_from_jwk_invalid_kty_raises():
    jwk = {"kty": "RSA", "k": "c2VjcmV0"}
    with pytest.raises(InvalidKeyError):
        HMACAlgorithm.from_jwk(jwk)

# Verifica exceção com input de tipo inválido
def test_from_jwk_invalid_input_type_raises():
    with pytest.raises(InvalidKeyError):
        HMACAlgorithm.from_jwk(123)
