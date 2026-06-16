import json
import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# verifica caminho feliz: entrada dict válida retorna os bytes decodificados
def test_from_jwk_happy_path_dict():
    jwk = {"kty": "oct", "k": "c2VjcmV0"}  # base64url de b'secret'
    assert HMACAlgorithm.from_jwk(jwk) == b"secret"

# verifica caminho feliz: entrada JSON string válida retorna os bytes decodificados
def test_from_jwk_happy_path_json_string():
    jwk_json = json.dumps({"kty": "oct", "k": "c2VjcmV0"})
    assert HMACAlgorithm.from_jwk(jwk_json) == b"secret"

# verifica exceção para chave de tipo não oct: Not an HMAC key
def test_from_jwk_invalid_kty_raises_InvalidKeyError():
    jwk = {"kty": "RSA", "k": "c2VjcmV0"}
    with pytest.raises(InvalidKeyError):
        HMACAlgorithm.from_jwk(jwk)

# valida exceção para entrada inválida (não é JSON válido)
def test_from_jwk_invalid_input_raises_InvalidKeyError():
    with pytest.raises(InvalidKeyError):
        HMACAlgorithm.from_jwk("not-json")
