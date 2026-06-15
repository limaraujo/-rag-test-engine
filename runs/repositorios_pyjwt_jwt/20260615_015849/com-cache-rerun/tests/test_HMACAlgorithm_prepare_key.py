import hashlib
import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm
import repositorios.pyjwt.jwt.algorithms as algs

import hashlib
import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

def test_prepare_key_happy_path():
    alg = HMACAlgorithm(hash_alg=hashlib.sha256)
    assert alg.prepare_key("secret") == b"secret"

def test_prepare_key_empty_raises():
    alg = HMACAlgorithm(hash_alg=hashlib.sha256)
    with pytest.raises(InvalidKeyError):
        alg.prepare_key("")

@pytest.mark.parametrize("key, should_raise", [
    ('{"kty":"oct","k":"v"}', True),
    ("   {not json}", False),
])
def test_prepare_key_jwk_related(key, should_raise):
    alg = HMACAlgorithm(hash_alg=hashlib.sha256)
    if should_raise:
        with pytest.raises(InvalidKeyError):
            alg.prepare_key(key)
    else:
        res = alg.prepare_key(key)
        assert res == key.encode()

@pytest.mark.parametrize("attr", ["is_pem_format", "is_ssh_key"])
def test_prepare_key_rejects_pem_or_ssh(monkeypatch, attr):
    import repositorios.pyjwt.jwt.algorithms as algs
    monkeypatch.setattr(algs, attr, lambda b: True)
    alg = HMACAlgorithm(hash_alg=hashlib.sha256)
    with pytest.raises(InvalidKeyError):
        alg.prepare_key("secret")
