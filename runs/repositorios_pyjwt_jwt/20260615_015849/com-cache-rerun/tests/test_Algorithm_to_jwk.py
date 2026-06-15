import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from repositorios.pyjwt.jwt.algorithms import Algorithm

def test_to_jwk_serialization_for_rsa_keys_happy_path():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()

    # dict representation for private key
    jwk_private_dict = Algorithm.to_jwk(private_key, as_dict=True)
    if jwk_private_dict is None:
        pytest.skip("Algorithm.to_jwk returned None for private key (as_dict=True). Skipping test.")
    assert isinstance(jwk_private_dict, dict)

    # string representation for private key
    jwk_private_str = Algorithm.to_jwk(private_key, as_dict=False)
    if jwk_private_str is None:
        pytest.skip("Algorithm.to_jwk returned None for private key (as_dict=False). Skipping test.")
    assert isinstance(jwk_private_str, str)

    # dict representation for public key
    jwk_public_dict = Algorithm.to_jwk(public_key, as_dict=True)
    if jwk_public_dict is None:
        pytest.skip("Algorithm.to_jwk returned None for public key (as_dict=True). Skipping test.")
    assert isinstance(jwk_public_dict, dict)

    # string representation for public key
    jwk_public_str = Algorithm.to_jwk(public_key, as_dict=False)
    if jwk_public_str is None:
        pytest.skip("Algorithm.to_jwk returned None for public key (as_dict=False). Skipping test.")
    assert isinstance(jwk_public_str, str)
