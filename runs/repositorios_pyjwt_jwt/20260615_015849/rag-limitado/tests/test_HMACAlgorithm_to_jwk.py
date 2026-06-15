import json
import base64
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm



def _encode_key(obj: bytes | str) -> str:
    data = obj.encode("utf-8") if isinstance(obj, str) else obj
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


# Teste 1: caminho feliz com chave str retornando dict
def test_hmac_to_jwk_dict_str_key():
    key = "secret"
    expected_k = _encode_key(key)
    result = HMACAlgorithm.to_jwk(key, as_dict=True)
    assert isinstance(result, dict)
    assert result["k"] == expected_k
    assert result["kty"] == "oct"


# Teste 2: caminho feliz com chave str retornando JSON
def test_hmac_to_jwk_json_str_key():
    key = "secret"
    expected_k = _encode_key(key)
    expected = {"k": expected_k, "kty": "oct"}
    json_str = HMACAlgorithm.to_jwk(key, as_dict=False)
    assert isinstance(json_str, str)
    assert json.loads(json_str) == expected


# Teste 3: chave em bytes é tratada corretamente
def test_hmac_to_jwk_dict_bytes_key():
    key = b"secretbytes"
    expected_k = _encode_key(key)
    result = HMACAlgorithm.to_jwk(key, as_dict=True)
    assert isinstance(result, dict)
    assert result["k"] == expected_k
    assert result["kty"] == "oct"


# Teste 4: caso de borda com chave vazia
def test_hmac_to_jwk_json_empty_key():
    key = ""
    expected = {"k": "", "kty": "oct"}
    json_str = HMACAlgorithm.to_jwk(key, as_dict=False)
    assert json.loads(json_str) == expected
