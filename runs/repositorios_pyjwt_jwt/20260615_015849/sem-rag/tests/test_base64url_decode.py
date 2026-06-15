import pytest
import repositorios.pyjwt.jwt.utils as jwt_utils
from repositorios.pyjwt.jwt.utils import base64url_decode

# short
# Testa caminho feliz: rem == 0 (nenhum padding adicional)
def test_base64url_decode_happy_path_no_padding(monkeypatch):
    def fake_force_bytes(value):
        if isinstance(value, str):
            return value.encode()
        return value

    monkeypatch.setattr(jwt_utils, "force_bytes", fake_force_bytes)
    result = jwt_utils.base64url_decode("SGVsbG8=")  # "Hello" com padding existente
    assert result == b"Hello"

# short
# Testa branch onde rem > 0 precisa adicionar padding
def test_base64url_decode_needs_padding(monkeypatch):
    def fake_force_bytes(value):
        if isinstance(value, str):
            return value.encode()
        return value

    monkeypatch.setattr(jwt_utils, "force_bytes", fake_force_bytes)
    result = jwt_utils.base64url_decode("SGVsbG8")  # sem padding
    assert result == b"Hello"

# short
# Testa entrada em bytes também funciona
def test_base64url_decode_bytes_input(monkeypatch):
    def fake_force_bytes(value):
        if isinstance(value, str):
            return value.encode()
        return value

    monkeypatch.setattr(jwt_utils, "force_bytes", fake_force_bytes)
    result = jwt_utils.base64url_decode(b"SGVsbG8")  # já sem padding, como bytes
    assert result == b"Hello"
