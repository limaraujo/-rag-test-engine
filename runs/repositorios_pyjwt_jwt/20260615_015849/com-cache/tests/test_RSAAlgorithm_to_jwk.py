import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

def _b64u(n: int) -> str:
    # helper para base64url de inteiros não-signados
    if n == 0:
        b = b'\x00'
    else:
        b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return base64.urlsafe_b64encode(b).decode('ascii').rstrip('=')

# Teste 1: chave RSA privada gera JWK com todos os componentes privados
# happy path: privada -> dict com n, e e d, p, q, dp, dq, qi
def test_to_jwk_private_includes_all_private_components():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    jwk = RSAAlgorithm.to_jwk(private_key, as_dict=True)

    assert isinstance(jwk, dict)
    assert jwk.get("kty") == "RSA"
    assert "n" in jwk and "e" in jwk
    nums = private_key.private_numbers()
    public_n = nums.public_numbers.n
    public_e = nums.public_numbers.e

    assert jwk["d"] == _b64u(nums.d)
    assert jwk["p"] == _b64u(nums.p)
    assert jwk["q"] == _b64u(nums.q)
    assert jwk["dp"] == _b64u(nums.dmp1)
    assert jwk["dq"] == _b64u(nums.dmq1)
    assert jwk["qi"] == _b64u(nums.iqmp)

    assert jwk["n"] == _b64u(public_n)
    assert jwk["e"] == _b64u(public_e)

# Teste 2: chave RSA pública gera JWK com apenas componentes públicos
# happy path: pública -> dict com n, e, sem componentes privados
def test_to_jwk_public_includes_only_public_components():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    jwk = RSAAlgorithm.to_jwk(public_key, as_dict=True)

    assert isinstance(jwk, dict)
    assert jwk.get("kty") == "RSA"
    assert "n" in jwk and "e" in jwk
    assert "d" not in jwk
    assert "p" not in jwk
    assert "q" not in jwk
    assert "dp" not in jwk
    assert "dq" not in jwk
    assert "qi" not in jwk

# Teste 3: chave RSA pública pode ser serializada como string JSON mantendo chaves públicas
# happy path: string JSON contém kty/n/e e não contém campos privados
def test_to_jwk_public_as_string_parses_and_contains_public_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    jwk_str = RSAAlgorithm.to_jwk(public_key, as_dict=False)

    assert isinstance(jwk_str, str)
    data = json.loads(jwk_str)
    assert data.get("kty") == "RSA"
    assert "n" in data and "e" in data
    assert "d" not in data
    assert "p" not in data
    assert "q" not in data
    assert "dp" not in data
    assert "dq" not in data
    assert "qi" not in data
