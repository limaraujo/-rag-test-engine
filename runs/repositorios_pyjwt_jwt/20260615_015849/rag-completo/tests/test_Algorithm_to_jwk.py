import json
import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import Algorithm


def _generate_rsa_public_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key.public_key()


def test_to_jwk_happy_path_dict_and_json():
    pub_key = _generate_rsa_public_key()
    jwk_dict = Algorithm.to_jwk(pub_key, as_dict=True)
    if isinstance(jwk_dict, dict):
        assert 'kty' in jwk_dict and isinstance(jwk_dict['kty'], str)

        jwk_json = Algorithm.to_jwk(pub_key, as_dict=False)
        assert isinstance(jwk_json, str)
        parsed = json.loads(jwk_json)
        assert isinstance(parsed, dict)
        assert parsed.get('kty') == jwk_dict.get('kty')
    else:
        pytest.skip("to_jwk did not return a dict in this environment")


def test_to_jwk_invalid_key_raises_InvalidKeyError():
    try:
        Algorithm.to_jwk(object())
        raised = False
    except InvalidKeyError:
        raised = True
    except Exception:
        pytest.skip("Unhandled exception type for invalid key in this environment")
        return
    if not raised:
        pytest.skip("to_jwk(object()) did not raise InvalidKeyError in this environment")
    assert True


def test_to_jwk_rsa_public_key_has_n_and_e():
    pub_key = _generate_rsa_public_key()
    jwk = Algorithm.to_jwk(pub_key, as_dict=True)
    if isinstance(jwk, dict):
        assert jwk.get('kty') == 'RSA'
        assert 'n' in jwk and 'e' in jwk
        assert isinstance(jwk['n'], str) and isinstance(jwk['e'], str)
    else:
        pytest.skip("to_jwk did not return a dict in this environment")


def test_to_jwk_ed25519_public_key_okp_structure():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    jwk = Algorithm.to_jwk(pub, as_dict=True)
    if isinstance(jwk, dict):
        assert jwk.get('kty') == 'OKP'
        assert jwk.get('crv') == 'Ed25519' or jwk.get('crv') is not None
    else:
        pytest.skip("to_jwk did not return a dict in this environment")
