import json
import base64
import pytest
import hashlib
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# Testa to_jwk cobrindo tanto input string/bytes quanto os modos as_dict True/False
@pytest.mark.parametrize("key_input, as_dict", [
    ("hello", True),
    (b"hello", True),
    ("hello", False),
    (b"hello", False),
])
def test_hmac_algorithm_to_jwk_key_input_and_flag(key_input, as_dict):
    # Fornece um hash_alg padrão para satisfazer o construtor
    algo = HMACAlgorithm(hashlib.sha256)
    raw_bytes = key_input if isinstance(key_input, (bytes, bytearray)) else key_input.encode("utf-8")
    expected_k = base64.urlsafe_b64encode(raw_bytes).rstrip(b"=").decode()

    if as_dict:
        result = algo.to_jwk(key_input, as_dict=True)
        assert isinstance(result, dict)
        assert result == {"k": expected_k, "kty": "oct"}
    else:
        result = algo.to_jwk(key_input, as_dict=False)
        expected_json = json.dumps({"k": expected_k, "kty": "oct"})
        assert result == expected_json
