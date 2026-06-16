import base64
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers, RSAPublicNumbers
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# curto: helper para criar uma RSA privada simples para testes
def _make_small_rsa_private_key():
    p = 3
    q = 11
    n = p * q  # 33
    e = 3
    d = 27
    dmp1 = d % (p - 1)  # 1
    dmq1 = d % (q - 1)  # 7
    iqmp = pow(q, -1, p)  # 2
    public_numbers = RSAPublicNumbers(e, n)
    private_numbers = RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public_numbers)
    return private_numbers.private_key(default_backend())

def _base64url_uint(n: int) -> str:
    if n == 0:
        b = b'\x00'
    else:
        b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return base64.urlsafe_b64encode(b).decode('ascii').rstrip('=')

# curto: happy path - RSA private key -> JWK dict with 'n'/'e' matching key
def test_to_jwk_happy_path():
    key = _make_small_rsa_private_key()
    jwk = RSAAlgorithm.to_jwk(key, as_dict=True)
    assert isinstance(jwk, dict)
    assert jwk.get('kty') == 'RSA'
    numbers = key.private_numbers().public_numbers
    expected_n = _base64url_uint(numbers.n)
    expected_e = _base64url_uint(numbers.e)
    assert jwk.get('n') == expected_n
    assert jwk.get('e') == expected_e

# curto: exceção esperada ao passar chave inválida
def test_to_jwk_invalid_key_raises():
    class NotRSA:
        pass
    with pytest.raises(InvalidKeyError):
        RSAAlgorithm.to_jwk(NotRSA(), as_dict=True)
