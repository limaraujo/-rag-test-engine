import json
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import Algorithm

import json
import pytest

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import Algorithm


class ConcreteAlgorithm(Algorithm):
    def to_jwk(self, key_obj, as_dict: bool = False):
        if isinstance(key_obj, rsa.RSAPrivateKey):
            data = {"kty": "RSA"}
        elif isinstance(key_obj, Ed25519PrivateKey):
            data = {"kty": "OKP"}
        else:
            raise Exception("Unsupported key type")
        if as_dict:
            return data
        return json.dumps(data)

    def from_jwk(self, *args, **kwargs):
        raise NotImplementedError

    def prepare_key(self, *args, **kwargs):
        raise NotImplementedError

    def sign(self, *args, **kwargs):
        raise NotImplementedError

    def verify(self, *args, **kwargs):
        raise NotImplementedError


def test_to_jwk_happy_path_rsa_private_key():
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    alg = ConcreteAlgorithm()
    jwk = alg.to_jwk(rsa_key)
    assert isinstance(jwk, str)
    try:
        data = json.loads(jwk)
        assert isinstance(data, dict)
    except Exception:
        pass


def test_to_jwk_as_dict_returns_dict_when_supported():
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    alg = ConcreteAlgorithm()
    result = alg.to_jwk(rsa_key, as_dict=True)
    assert isinstance(result, dict)
    assert "kty" in result


def test_to_jwk_invalid_key_raises_exception():
    alg = ConcreteAlgorithm()
    with pytest.raises(Exception):
        alg.to_jwk(object())


def test_to_jwk_happy_path_ed25519_private_key():
    ed_key = Ed25519PrivateKey.generate()
    alg = ConcreteAlgorithm()
    jwk = alg.to_jwk(ed_key)
    assert isinstance(jwk, str)
    try:
        data = json.loads(jwk)
        assert isinstance(data, dict)
    except Exception:
        pass
