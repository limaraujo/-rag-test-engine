import json
import pytest
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm


# Teste: caminho feliz - chave EC pública gera JWK em formato JSON com campos esperados
def test_to_jwk_happy_path_public_key_json():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    jwk_json = ECAlgorithm.to_jwk(public_key)
    assert isinstance(jwk_json, str)
    data = json.loads(jwk_json)
    assert data.get("kty") == "EC"
    assert data.get("crv") in {"P-256", "P-256K"} or data.get("crv") == "P-256"
    assert "x" in data and "y" in data
    assert isinstance(data["x"], str) and isinstance(data["y"], str)

# Teste: caminho feliz com as_dict=True retorna dicionário com campos esperados
def test_to_jwk_happy_path_as_dict_true_returns_dict():
    public_key = ec.generate_private_key(ec.SECP256R1()).public_key()
    jwk_dict = ECAlgorithm.to_jwk(public_key, as_dict=True)
    assert isinstance(jwk_dict, dict)
    assert jwk_dict.get("kty") == "EC"
    assert "x" in jwk_dict and "y" in jwk_dict

# Teste: exceção é lançada para tipo de chave não EC (RSA)
def test_to_jwk_unsupported_key_type_raises():
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with pytest.raises(Exception):
        ECAlgorithm.to_jwk(rsa_key)
