import pytest
from repositorios.pyjwt.jwt.utils import force_bytes


# curto: string -> bytes (caminho feliz)
def test_force_bytes_string_happy_path():
    s = "hello"
    assert force_bytes(s) == b"hello"
    assert isinstance(force_bytes(s), bytes)

# curto: bytes -> passthrough (branch elif)
def test_force_bytes_bytes_passthrough_identity():
    b = b"world"
    result = force_bytes(b)
    assert result is b

# curto: tipo inválido -> TypeError (branch else)
def test_force_bytes_invalid_type_raises_typeerror():
    with pytest.raises(TypeError):
        force_bytes(123)
