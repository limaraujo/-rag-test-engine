from repositorios.pyjwt.jwt.utils import base64url_encode

# happy path: verifica encode básico de um input comum e remoção de padding
def test_base64url_encode_happy_path():
    input_bytes = b"hello"
    expected = b"aGVsbG8"
    assert base64url_encode(input_bytes) == expected

# edge case: entrada vazia retorna bytes vazios
def test_base64url_encode_empty_input():
    assert base64url_encode(b"") == b""

# padding removal: verifica que '=' é removido quando presente (input que gera padding)
def test_base64url_encode_removes_padding():
    assert base64url_encode(b"abcd") == b"YWJjZA"
