import pytest
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from repositorios.pyjwt.jwt.utils import der_to_raw_signature

class DummyCurve:
    def __init__(self, key_size: int):
        self.key_size = key_size

# Verifica o caminho feliz: converte DER para RAW para curvas de 160/256 bits com r=1, s=2
@pytest.mark.parametrize("key_size", [160, 256])
def test_der_to_raw_signature_happy_path(key_size):
    r = 1
    s = 2
    der_sig = encode_dss_signature(r, s)
    curve = DummyCurve(key_size)

    raw = der_to_raw_signature(der_sig, curve)

    num_bytes = (key_size + 7) // 8
    expected = r.to_bytes(num_bytes, byteorder="big") + s.to_bytes(num_bytes, byteorder="big")

    assert raw == expected
    assert len(raw) == 2 * num_bytes
