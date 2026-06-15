import base64
from cryptography.hazmat.primitives.asymmetric import ec
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# short: happy path with SECP256R1 public key
def test_to_jwk_happy_path_secp256r1():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    jwk = ECAlgorithm.to_jwk(public_key, as_dict=True)

    assert isinstance(jwk, dict)
    assert jwk.get("kty") == "EC"
    assert jwk.get("crv") == "P-256"
    assert "x" in jwk and "y" in jwk

    pn = public_key.public_numbers()
    x_bytes = pn.x.to_bytes((pn.x.bit_length() + 7) // 8, "big")
    y_bytes = pn.y.to_bytes((pn.y.bit_length() + 7) // 8, "big")
    expected_x = base64.urlsafe_b64encode(x_bytes).decode("ascii").rstrip("=")
    expected_y = base64.urlsafe_b64encode(y_bytes).decode("ascii").rstrip("=")

    assert jwk["x"] == expected_x
    assert jwk["y"] == expected_y
