import pytest
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from repositorios.pyjwt.jwt.utils import raw_to_der_signature

class DummyCurve:
    def __init__(self, key_size: int):
        self.key_size = key_size

# short: happy path with 256-bit curve
def test_happy_path_256():
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    r = 1
    s = 2
    raw_sig = r.to_bytes(num_bytes, "big") + s.to_bytes(num_bytes, "big")
    expected_der = encode_dss_signature(r, s)
    assert raw_to_der_signature(raw_sig, curve) == expected_der

# short: happy path with 384-bit curve
def test_happy_path_384():
    curve = DummyCurve(384)
    num_bytes = (curve.key_size + 7) // 8
    r = 3
    s = 5
    raw_sig = r.to_bytes(num_bytes, "big") + s.to_bytes(num_bytes, "big")
    expected_der = encode_dss_signature(r, s)
    assert raw_to_der_signature(raw_sig, curve) == expected_der

# short: invalid input length should raise ValueError
def test_invalid_input_length_raises_value_error():
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    raw_sig = b"\x00" * ((num_bytes * 2) - 1)  # one byte short
    with pytest.raises(ValueError):
        raw_to_der_signature(raw_sig, curve)
