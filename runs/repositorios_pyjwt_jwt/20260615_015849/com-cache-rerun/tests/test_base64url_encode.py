import pytest
from repositorios.pyjwt.jwt.utils import base64url_encode

# curto: happy path - encode simples sem padding
def test_base64url_encode_happy_path():
    assert base64url_encode(b"Hello") == b"SGVsbG8"

# curto: remove padding quando a entrada geraria padding na base64 padrão
def test_base64url_encode_removes_padding():
    assert base64url_encode(b"test") == b"dGVzdA"

# curto: encode de entrada vazia resulta em saída vazia
def test_base64url_encode_empty_input():
    assert base64url_encode(b"") == b""

# curto: falha ao receber tipo incorreto (TypeError)
def test_base64url_encode_wrong_type_raises():
    with pytest.raises(TypeError):
        base64url_encode("Hello")
