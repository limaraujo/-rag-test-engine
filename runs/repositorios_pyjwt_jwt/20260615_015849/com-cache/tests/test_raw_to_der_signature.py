import pytest
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from repositorios.pyjwt.jwt.utils import raw_to_der_signature

import pytest

from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from repositorios.pyjwt.jwt.utils import raw_to_der_signature


class DummyCurve:
    def __init__(self, key_size: int):
        self.key_size = key_size


def int_to_bytes(num: int, length: int) -> bytes:
    return num.to_bytes(length, byteorder="big")


# Test 1: happy path - valid raw signature converts to DER signature for given curve
# cenário: happy path com curva de tamanho 256 bits
def test_raw_to_der_signature_happy_path():
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    r = 1
    s = 2
    raw_sig = int_to_bytes(r, num_bytes) + int_to_bytes(s, num_bytes)

    expected_der = encode_dss_signature(r, s)
    der_sig = raw_to_der_signature(raw_sig, curve)

    assert der_sig == expected_der


# Test 2: invalid input length - should raise ValueError when raw signature length is incorrect
# cenári o borda: input inválido (comprimento incorreto)
def test_raw_to_der_signature_invalid_input_length():
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    raw_sig = b"\x00" * (2 * num_bytes - 1)  # one byte short

    with pytest.raises(ValueError):
        raw_to_der_signature(raw_sig, curve)
