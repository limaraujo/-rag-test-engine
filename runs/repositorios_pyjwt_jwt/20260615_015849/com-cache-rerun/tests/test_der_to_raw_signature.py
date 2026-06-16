import pytest
import binascii
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from repositorios.pyjwt.jwt.utils import der_to_raw_signature

def number_to_bytes(num: int, num_bytes: int) -> bytes:
    padded_hex = "%0*x" % (2 * num_bytes, num)
    return binascii.a2b_hex(padded_hex.encode("ascii"))

class FakeCurve:
    def __init__(self, key_size: int):
        self.key_size = key_size

def test_der_to_raw_signature_happy_path():
    r, s = 123456789, 987654321
    der_sig = encode_dss_signature(r, s)
    curve = FakeCurve(256)
    raw = der_to_raw_signature(der_sig, curve)
    num_bytes = (curve.key_size + 7) // 8
    r_dec, s_dec = decode_dss_signature(der_sig)
    expected = number_to_bytes(r_dec, num_bytes) + number_to_bytes(s_dec, num_bytes)
    assert raw == expected

def test_der_to_raw_signature_invalid_der_raises_value_error():
    curve = FakeCurve(256)
    with pytest.raises(ValueError):
        der_to_raw_signature(b"", curve)

@pytest.mark.parametrize("key_size", [256, 384, 521])
def test_der_to_raw_signature_scaling(key_size):
    r, s = 1, 2
    der_sig = encode_dss_signature(r, s)
    curve = FakeCurve(key_size)
    raw = der_to_raw_signature(der_sig, curve)
    num_bytes = (key_size + 7) // 8
    r_dec, s_dec = decode_dss_signature(der_sig)
    expected = number_to_bytes(r_dec, num_bytes) + number_to_bytes(s_dec, num_bytes)
    assert raw == expected
