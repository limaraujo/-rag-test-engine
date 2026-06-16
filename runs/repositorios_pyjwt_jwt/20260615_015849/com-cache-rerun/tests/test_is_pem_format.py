import pytest
from repositorios.pyjwt.jwt.utils import is_pem_format

# curto: happy path - PEM com CERTIFICATE reconhecido
def test_is_pem_format_true_certificate():
    pem_cert = (
        b"-----BEGIN CERTIFICATE-----\n"
        b"MIIBIjANBknwH0k5Qf9a3Q==\n"
        b"-----END CERTIFICATE-----\n"
    )
    assert is_pem_format(pem_cert)

# curto: happy path - PEM com PRIVATE KEY reconhecido
def test_is_pem_format_true_private_key():
    pem_priv = (
        b"-----BEGIN RSA PRIVATE KEY-----\n"
        b"MIIEpAIBAAKCAQEA7f1\n"
        b"-----END RSA PRIVATE KEY-----\n"
    )
    assert is_pem_format(pem_priv)

# curto: casos negativos - entrada vazia ou não-PEM
@pytest.mark.parametrize("data", [
    b"",
    b"not a pem data"
])
def test_is_pem_format_false_for_non_pem_or_empty(data):
    # negado: não é PEM válido
    assert not is_pem_format(data)
