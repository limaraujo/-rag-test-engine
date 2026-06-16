import base64
import pytest
from repositorios.pyjwt.jwt.utils import to_base64url_uint


# verifica comportamento com input negativo: lança ValueError
def test_to_base64url_uint_negative_raises_value_error():
    with pytest.raises(ValueError):
        to_base64url_uint(-1)

# verifica caminho com zero: retorna base64url de 0 -> b'AA'
def test_to_base64url_uint_zero_returns_aa():
    assert to_base64url_uint(0) == b"AA"

# verifica valor pequeno (1) resulta em 'AQ'
def test_to_base64url_uint_one_returns_aq():
    expected = base64.urlsafe_b64encode(b"\x01").replace(b"=", b"")
    assert to_base64url_uint(1) == expected

# verifica uso de bit_length com val=0xff produz base64url de dois bytes
def test_to_base64url_uint_with_bit_length():
    val = 0xFF
    bit_length = 16
    expected = base64.urlsafe_b64encode(b"\x00\xff").replace(b"=", b"")
    assert to_base64url_uint(val, bit_length=bit_length) == expected
