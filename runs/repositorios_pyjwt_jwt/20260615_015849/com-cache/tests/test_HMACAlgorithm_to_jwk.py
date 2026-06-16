import json
import base64
import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


# curto: valida o caminho principal (happy path) e o fallback de método/instância
def _invoke_to_jwk(key_input, as_dict):
    try:
        return HMACAlgorithm.to_jwk(key_input, as_dict=as_dict)
    except TypeError:
        return HMACAlgorithm().to_jwk(key_input, as_dict=as_dict)

def _expected_k(key_input):
    b = key_input.encode() if isinstance(key_input, str) else key_input
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

@pytest.mark.parametrize("key_input", ["secret", b"secret"])
@pytest.mark.parametrize("as_dict", [True, False])
def test_hmac_algorithm_to_jwk_key_formats(key_input, as_dict):
    # curto: verifica both branches (dict vs json string) com diferentes tipos de chave
    result = _invoke_to_jwk(key_input, as_dict=as_dict)
    expected_k = _expected_k(key_input)

    if as_dict:
        assert isinstance(result, dict)
        assert result.get("kty") == "oct"
        assert result.get("k") == expected_k
        # espera apenas as chaves utilizadas
        assert set(result.keys()) == {"k", "kty"}
    else:
        assert isinstance(result, str)
        data = json.loads(result)
        assert data == {"k": expected_k, "kty": "oct"}
