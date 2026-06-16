from repositorios.pyjwt.jwt.utils import base64url_encode

# happy path: input 'foo' sem padding a ser removido
def test_base64url_encode_happy_path_foo():
    input_data = b"foo"
    expected = b"Zm9v"
    assert base64url_encode(input_data) == expected

# padding removal: input que gera '=' e precisa remover
def test_base64url_encode_removes_padding():
    input_data = b"fo"
    expected = b"Zm8"
    assert base64url_encode(input_data) == expected

# edge case: entrada vazia
def test_base64url_encode_empty_input():
    assert base64url_encode(b"") == b""

# zero byte: 0x00 deve produzir 'AA' após remoção de padding
def test_base64url_encode_zero_byte():
    assert base64url_encode(b"\x00") == b"AA"
