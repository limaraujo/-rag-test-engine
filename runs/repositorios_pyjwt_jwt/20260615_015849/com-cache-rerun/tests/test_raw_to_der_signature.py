import pytest
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from repositorios.pyjwt.jwt.utils import raw_to_der_signature

def int_to_fixed_bytes(value: int, length: int) -> bytes:
    return value.to_bytes(length, byteorder="big")

class DummyCurve:
    def __init__(self, key_size: int):
        self.key_size = key_size

# Verifica caminho feliz: converte assinatura bruta de 2*num_bytes para DER corretamente (curva de 256 bits)
def test_raw_to_der_signature_happy_path():
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    r = 1
    s = 2
    raw_sig = int_to_fixed_bytes(r, num_bytes) + int_to_fixed_bytes(s, num_bytes)
    der = raw_to_der_signature(raw_sig, curve)
    assert decode_dss_signature(der) == (r, s)

# Verifica comportamento de erro: input com tamanho inválido deve levantar ValueError
def test_raw_to_der_signature_invalid_input_raises_value_error():
    curve = DummyCurve(256)
    num_bytes = (curve.key_size + 7) // 8
    raw_sig = b'\x01' * (2 * num_bytes - 1)  # inválido: tamanho incorreto
    with pytest.raises(ValueError):
        raw_to_der_signature(raw_sig, curve)
