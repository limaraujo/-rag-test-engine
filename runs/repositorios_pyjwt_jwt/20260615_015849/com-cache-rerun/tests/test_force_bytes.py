import pytest
from repositorios.pyjwt.jwt.utils import force_bytes

# Verifica: converte string não-ASCII para bytes UTF-8 (happy path para str)
def test_force_bytes_from_str_utf8():
    s = "áéñ"
    assert force_bytes(s) == s.encode("utf-8")

# Verifica: retorna os bytes já fornecidos (caminho branch bytes)
def test_force_bytes_from_bytes_passthrough():
    b = b"abc"
    assert force_bytes(b) == b

# Verifica: lança TypeError quando o tipo não suportado é passado (caso de borda)
def test_force_bytes_raises_type_error_for_invalid_type():
    with pytest.raises(TypeError):
        force_bytes(123)
