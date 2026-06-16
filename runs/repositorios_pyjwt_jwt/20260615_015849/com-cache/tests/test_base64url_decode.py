import pytest
from repositorios.pyjwt.jwt.utils import base64url_decode

# Verifica que decodifica com entrada sem padding (rem > 0)
def test_base64url_decode_rem_gt_zero():
    s = "SGVsbG8"  # "Hello" sem padding
    assert base64url_decode(s) == b"Hello"

# Verifica que decodifica quando o input já tem padding correto (rem == 0)
def test_base64url_decode_rem_eq_zero():
    s = "SGVsbG8="
    assert base64url_decode(s) == b"Hello"

# Verifica que entradas de tipo inválido levantam TypeError via force_bytes
def test_base64url_decode_invalid_input_type_raises_type_error():
    with pytest.raises(TypeError):
        base64url_decode(123)
