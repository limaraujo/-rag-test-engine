import pytest
from repositorios.pyjwt.jwt.utils import force_bytes

# Teste feliz: converte string para bytes usando UTF-8
def test_force_bytes_from_str():
    s = "áéñ"
    assert force_bytes(s) == s.encode("utf-8")

# Teste já é bytes: retorna exatamente os bytes fornecidos
def test_force_bytes_from_bytes():
    data = b"byte-string"
    assert force_bytes(data) == data

# Teste com tipo inválido levanta TypeError
def test_force_bytes_invalid_type_raises_typeerror():
    with pytest.raises(TypeError):
        force_bytes(123)
