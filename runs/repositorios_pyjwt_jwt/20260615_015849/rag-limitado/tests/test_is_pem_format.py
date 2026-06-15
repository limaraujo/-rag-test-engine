from repositorios.pyjwt.jwt.utils import is_pem_format

# happy path: PEM formatado válido deve retornar True
def test_is_pem_format_true_happy_path():
    pem = b"-----BEGIN CERTIFICATE-----\nMIIBIjANB...certificate...==\n-----END CERTIFICATE-----\n"
    assert is_pem_format(pem) is True

# edge case: bytes que não contêm PEM devem retornar False
def test_is_pem_format_false_non_pem():
    data = b"This is not a PEM formatted key"
    assert is_pem_format(data) is False

# edge case: entrada vazia deve retornar False
def test_is_pem_format_false_empty():
    assert is_pem_format(b"") is False

# edge case: PEM iniciado mas sem fim (incomplete PEM) deve retornar False
def test_is_pem_format_false_incomplete_pem():
    incomplete = b"-----BEGIN CERTIFICATE-----\nMIIBIjA"
    assert is_pem_format(incomplete) is False
