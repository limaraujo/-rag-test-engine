import base64
import pytest
from repositorios.pyjwt.jwt.utils import to_base64url_uint



# curto: caminho feliz com 0 retorna base64url de 0x00 sem padding
def test_to_base64url_uint_zero():
    assert to_base64url_uint(0) == b"AA"


# curto: caminho feliz com 1 sem especificar bit_length
def test_to_base64url_uint_one_no_bit_length():
    assert to_base64url_uint(1) == b"AQ"


# curto: cenário com bit_length extra (8 bits adicionais, resultando em 0x0001)
def test_to_base64url_uint_one_with_bit_length_16():
    expected = base64.urlsafe_b64encode(b"\x00\x01").replace(b"=", b"")
    assert to_base64url_uint(1, bit_length=16) == expected


# curto: erro ao passar valor negativo
def test_to_base64url_uint_negative_raises():
    with pytest.raises(ValueError, match="Must be a positive integer"):
        to_base64url_uint(-1)
