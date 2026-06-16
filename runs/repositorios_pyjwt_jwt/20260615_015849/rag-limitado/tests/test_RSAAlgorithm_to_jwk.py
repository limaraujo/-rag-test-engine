import json
import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt import utils as jwt_utils
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

import json
import pytest

from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt import utils as jwt_utils
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm


# helper mocks
class MockPrivateKey:
    def __init__(self, n, e, d, p, q, dmp1, dmq1, iqmp):
        pub = type("Pub", (), {"n": n, "e": e})()
        priv = type(
            "Priv",
            (),
            {
                "public_numbers": pub,
                "d": d,
                "p": p,
                "q": q,
                "dmp1": dmp1,
                "dmq1": dmq1,
                "iqmp": iqmp,
            },
        )
        self._priv = priv

    def private_numbers(self):
        return self._priv


class MockPublicKey:
    def __init__(self, n, e):
        self._pub = type("Pub", (), {"n": n, "e": e})()
        # provide verify to satisfy hasattr(key_obj, "verify")
        self.verify = lambda *args, **kwargs: None

    def public_numbers(self):
        return self._pub


class EmptyKey:
    pass


# Test 1: private key path, as_dict=True (happy path)
# verifica que para chave privada retorna dict com campos RSA esperados
def test_to_jwk_private_as_dict():
    n, e = 65537, 3
    d, p, q = 12345, 5, 7
    dmp1, dmq1, iqmp = 1, 2, 3

    private_key = MockPrivateKey(n, e, d, p, q, dmp1, dmq1, iqmp)

    expected = {
        "kty": "RSA",
        "key_ops": ["sign"],
        "n": jwt_utils.to_base64url_uint(n).decode(),
        "e": jwt_utils.to_base64url_uint(e).decode(),
        "d": jwt_utils.to_base64url_uint(d).decode(),
        "p": jwt_utils.to_base64url_uint(p).decode(),
        "q": jwt_utils.to_base64url_uint(q).decode(),
        "dp": jwt_utils.to_base64url_uint(dmp1).decode(),
        "dq": jwt_utils.to_base64url_uint(dmq1).decode(),
        "qi": jwt_utils.to_base64url_uint(iqmp).decode(),
    }

    result = RSAAlgorithm.to_jwk(private_key, as_dict=True)
    assert result == expected


# Test 2: private key path, as_dict=False (string JSON)
# verifica que a saída é uma string JSON contendo os campos esperados
def test_to_jwk_private_as_json_string():
    n, e = 65537, 3
    d, p, q = 12345, 5, 7
    dmp1, dmq1, iqmp = 1, 2, 3

    private_key = MockPrivateKey(n, e, d, p, q, dmp1, dmq1, iqmp)

    expected = {
        "kty": "RSA",
        "key_ops": ["sign"],
        "n": jwt_utils.to_base64url_uint(n).decode(),
        "e": jwt_utils.to_base64url_uint(e).decode(),
        "d": jwt_utils.to_base64url_uint(d).decode(),
        "p": jwt_utils.to_base64url_uint(p).decode(),
        "q": jwt_utils.to_base64url_uint(q).decode(),
        "dp": jwt_utils.to_base64url_uint(dmp1).decode(),
        "dq": jwt_utils.to_base64url_uint(dmq1).decode(),
        "qi": jwt_utils.to_base64url_uint(iqmp).decode(),
    }

    result_str = RSAAlgorithm.to_jwk(private_key, as_dict=False)
    parsed = json.loads(result_str)
    assert parsed == expected


# Test 3: public key path, as_dict=True
# verifica que para chave pública retorna dict com operações de verificação
def test_to_jwk_public_as_dict():
    n, e = 65539, 17
    public_key = MockPublicKey(n, e)

    expected = {
        "kty": "RSA",
        "key_ops": ["verify"],
        "n": jwt_utils.to_base64url_uint(n).decode(),
        "e": jwt_utils.to_base64url_uint(e).decode(),
    }

    result = RSAAlgorithm.to_jwk(public_key, as_dict=True)
    assert result == expected


# Test 4: chave inválida lança InvalidKeyError
# verifica comportamento de borda quando o objeto não é chave RSA
def test_to_jwk_invalid_key_raises():
    bad = EmptyKey()
    with pytest.raises(InvalidKeyError):
        RSAAlgorithm.to_jwk(bad)
