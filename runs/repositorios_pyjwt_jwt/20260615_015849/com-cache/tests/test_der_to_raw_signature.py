import binascii
from repositorios.pyjwt.jwt.utils import der_to_raw_signature

def number_to_bytes(num: int, num_bytes: int) -> bytes:
    padded_hex = "%0*x" % (2 * num_bytes, num)
    return binascii.a2b_hex(padded_hex.encode("ascii"))

class DummyCurve:
    def __init__(self, key_size: int):
        self.key_size = key_size

def test_der_to_raw_signature_basic():
    der_sig = bytes([0x30, 0x06, 0x02, 0x01, 0x01, 0x02, 0x01, 0x02])
    curve = DummyCurve(256)
    result = der_to_raw_signature(der_sig, curve)
    expected = number_to_bytes(1, 32) + number_to_bytes(2, 32)
    assert result == expected

def test_der_to_raw_signature_large_key_size_padding():
    der_sig = bytes([0x30, 0x06, 0x02, 0x01, 0x01, 0x02, 0x01, 0x02])
    curve = DummyCurve(512)
    result = der_to_raw_signature(der_sig, curve)
    expected = number_to_bytes(1, 64) + number_to_bytes(2, 64)
    assert result == expected
