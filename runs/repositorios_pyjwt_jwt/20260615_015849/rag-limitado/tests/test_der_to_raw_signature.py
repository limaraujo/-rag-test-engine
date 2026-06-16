import pytest
from types import SimpleNamespace
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from repositorios.pyjwt.jwt.utils import der_to_raw_signature


# happy path: 256-bit curve, small r and s values
def test_der_to_raw_signature_256bit_happy_path():
    # short: verifies correct concatenation and padding to 32 bytes each
    r = 1
    s = 2
    der = encode_dss_signature(r, s)
    curve = SimpleNamespace(key_size=256)
    raw = der_to_raw_signature(der, curve)
    expected = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    assert raw == expected

# happy path: 384-bit curve, small r and s values
def test_der_to_raw_signature_384bit_happy_path():
    # long: verifies correct padding to 48 bytes each for 384-bit curve
    r = 1
    s = 2
    der = encode_dss_signature(r, s)
    curve = SimpleNamespace(key_size=384)
    raw = der_to_raw_signature(der, curve)
    expected = r.to_bytes(48, "big") + s.to_bytes(48, "big")
    assert raw == expected

# error handling: invalid DER should raise a ValueError from decode_dss_signature
def test_der_to_raw_signature_invalid_der_raises():
    # invalid input: ensure function propagates decode error
    der = b"not-an-der"
    curve = SimpleNamespace(key_size=256)
    with pytest.raises(ValueError):
        der_to_raw_signature(der, curve)
