import pytest
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from repositorios.pyjwt.jwt.utils import raw_to_der_signature

class DummyCurve:
    def __init__(self, key_size: int):
        self.key_size = key_size

# happy path: valid raw signature converts to DER for 256-bit curve
def test_raw_to_der_signature_happy_path():
    # short: verify correct DER encoding for valid inputs
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    r = 1
    s = 2
    raw_sig = r.to_bytes(num_bytes, 'big') + s.to_bytes(num_bytes, 'big')
    expected_der = encode_dss_signature(r, s)
    assert raw_to_der_signature(raw_sig, curve) == expected_der

# edge case: invalid input length raises ValueError
def test_raw_to_der_signature_invalid_input_length():
    # edge: input length not equal to 2 * num_bytes should raise
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    raw_sig = b'\x00' * (2 * num_bytes - 1)
    with pytest.raises(ValueError, match="Invalid signature"):
        raw_to_der_signature(raw_sig, curve)

# boundary: all max bytes for r and s are encoded to a DER signature
def test_raw_to_der_signature_all_ones():
    # boundary: ensure large values are handled without error
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    r = 2**(8 * num_bytes) - 1
    s = r
    raw_sig = r.to_bytes(num_bytes, 'big') + s.to_bytes(num_bytes, 'big')
    expected_der = encode_dss_signature(r, s)
    assert raw_to_der_signature(raw_sig, curve) == expected_der
