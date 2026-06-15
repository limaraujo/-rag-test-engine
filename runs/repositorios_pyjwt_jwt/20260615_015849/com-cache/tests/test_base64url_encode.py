from repositorios.pyjwt.jwt.utils import base64url_encode

# teste de caminho feliz: encode simples sem padding
def test_base64url_encode_happy_path():
    assert base64url_encode(b"Hello") == b"SGVsbG8"

# teste de remoção de padding: entrada que resulta em um '=' antes da remoção
def test_base64url_encode_removes_padding():
    assert base64url_encode(b"Hi") == b"SGk"

# teste de caso de borda: entrada vazia
def test_base64url_encode_empty_input():
    assert base64url_encode(b"") == b""
