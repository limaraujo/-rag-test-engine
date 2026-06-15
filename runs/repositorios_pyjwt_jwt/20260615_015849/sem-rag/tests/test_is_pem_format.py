import pytest
from repositorios.pyjwt.jwt.utils import is_pem_format

# Verifica diferentes cenários: PEMs válidos (certificado/public key) vs. não-PEM e vazio (caminho feliz e casos de borda)
@pytest.mark.parametrize("data, expected", [
    (b"-----BEGIN CERTIFICATE-----\nMIIBIjANB...==\n-----END CERTIFICATE-----\n", True),
    (b"-----BEGIN PUBLIC KEY-----\nMIGfMA0G...==\n-----END PUBLIC KEY-----\n", True),
    (b"this is not PEM data", False),
    (b"", False),
])
def test_is_pem_format_various_inputs(data, expected):
    assert is_pem_format(data) is expected
