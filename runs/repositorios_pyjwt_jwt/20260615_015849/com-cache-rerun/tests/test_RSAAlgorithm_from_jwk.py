import pytest
import repositorios.pyjwt.jwt.algorithms as algorithms
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

RSAAlgorithm = algorithms.RSAAlgorithm
InvalidKeyError = getattr(algorithms, "InvalidKeyError")

# curto
def test_from_jwk_private_key_happy_path(monkeypatch):
    class DummyPublicNumbers:
        def __init__(self, e, n):
            self.e = e
            self.n = n

    class DummyPrivateNumbers:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
        def private_key(self):
            return "PRIVATE_KEY"

    monkeypatch.setattr(algorithms, "RSAPublicNumbers", DummyPublicNumbers, raising=True)
    monkeypatch.setattr(algorithms, "RSAPrivateNumbers", DummyPrivateNumbers, raising=True)
    monkeypatch.setattr(algorithms, "from_base64url_uint", lambda x: x, raising=True)

    jwk = {
        "kty": "RSA",
        "n": 123,
        "e": 65537,
        "d": 987,
        "p": 11,
        "q": 13,
        "dp": 17,
        "dq": 19,
        "qi": 23,
    }

    assert RSAAlgorithm.from_jwk(jwk) == "PRIVATE_KEY"

# curto
def test_from_jwk_invalid_json_raises():
    with pytest.raises(InvalidKeyError) as exc:
        RSAAlgorithm.from_jwk("not json")
    assert "Key is not valid JSON" in str(exc.value)

# curto
def test_from_jwk_not_rsa_raises():
    jwk = {"kty": "EC", "n": 1, "e": 1}
    with pytest.raises(InvalidKeyError) as exc:
        RSAAlgorithm.from_jwk(jwk)
    assert "Not an RSA key" in str(exc.value)

# curto
def test_from_jwk_incomplete_private_params_raises():
    jwk = {"kty": "RSA", "n": 1, "e": 1, "d": 1, "p": 2}  # has p but missing other params
    with pytest.raises(InvalidKeyError) as exc:
        RSAAlgorithm.from_jwk(jwk)
    assert "RSA key must include all parameters" in str(exc.value)
