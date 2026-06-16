import json
import base64
import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


def _force_bytes(obj: str | bytes) -> bytes:
    return obj.encode("utf-8") if isinstance(obj, str) else obj


def _base64url_encode_bytes(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


@pytest.mark.parametrize("key_obj, as_dict", [
    ("mysecret", True),
    ("mysecret", False),
    (b"mysecret", True),
    ("ünícødë", True),
])
# Verifica HMACAlgorithm.to_jwk gera dict quando as_dict=True e JSON string quando False
# cobrindo casos de entrada em str/bytes e dados com ASCII/non-ASCII
def test_hmac_algorithm_to_jwk_outputs(key_obj, as_dict):
    expected = {
        "k": _base64url_encode_bytes(_force_bytes(key_obj)),
        "kty": "oct",
    }

    result = HMACAlgorithm.to_jwk(key_obj, as_dict=as_dict)

    if as_dict:
        assert isinstance(result, dict)
        assert result == expected
    else:
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == expected
