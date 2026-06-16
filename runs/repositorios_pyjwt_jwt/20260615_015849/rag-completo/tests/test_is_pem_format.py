import pytest
from repositorios.pyjwt.jwt.utils import is_pem_format

# happy path: detect multiple PEM formats (BEGIN PUBLIC KEY and BEGIN CERTIFICATE)
@pytest.mark.parametrize("pem_bytes", [
    b"-----BEGIN PUBLIC KEY-----\nMIIBIjANB\n-----END PUBLIC KEY-----\n",
    b"-----BEGIN CERTIFICATE-----\nMIIBIjANB\nMIIB\n-----END CERTIFICATE-----\n",
])
def test_is_pem_format_true_for_pem_variants(pem_bytes):
    assert is_pem_format(pem_bytes) is True

# negative case: non-PEM data should return False
def test_is_pem_format_false_for_non_pem():
    assert is_pem_format(b"not-a-pem-data") is False

# edge case: incomplete PEM without an END marker should be False
def test_is_pem_format_false_when_end_marker_missing():
    assert is_pem_format(b"-----BEGIN CERTIFICATE-----\nMIIBIjANB\n") is False
