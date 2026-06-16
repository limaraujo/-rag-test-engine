import pytest
from repositorios.pyjwt.jwt.utils import is_pem_format

# curto: verifica is_pem_format retorna True para PEM válido e False para não-PEM/vazio
@pytest.mark.parametrize("key,expected", [
    (
        b"-----BEGIN CERTIFICATE-----\nMIIBIjANBKNwH0k5Qf9a3Q==\n-----END CERTIFICATE-----\n",
        True
    ),
    (b"not a pem", False),
    (b"", False),
])
def test_is_pem_format_various(key, expected):
    assert is_pem_format(key) == expected
