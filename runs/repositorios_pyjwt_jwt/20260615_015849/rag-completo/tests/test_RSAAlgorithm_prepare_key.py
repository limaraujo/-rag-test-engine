import pytest
import importlib
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# Verifica múltiplos cenários de RSAAlgorithm.prepare_key (caminho feliz, ssh-rsa, PEM privada, input inválido)

@pytest.mark.parametrize("scenario", [
    "crypto_key_instance",
    "ssh_rsa_path",
    "pem_private_path",
    "invalid_input_raises_InvalidKeyError",
])
def test_prepare_key_various_scenarios(scenario, monkeypatch):
    algorithms = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    # Helpers para criar selfs simulados
    class DummySelf:
        def __init__(self, crypto_type):
            self._crypto_key_types = (crypto_type,)
            self.checked = []
        def check_crypto_key_type(self, key):
            self.check_called_with = key
            self.checked.append(key)

    class NotCryptoKey:
        pass

    # Cenário A: chave já é um tipo criptográfico suportado
    if scenario == "crypto_key_instance":
        DummyRSAPublicKey = type("DummyRSAPublicKey", (), {})
        key = DummyRSAPublicKey()
        self_sim = DummySelf(DummyRSAPublicKey)

        result = algorithms.RSAAlgorithm.prepare_key(self_sim, key)
        assert result is key

        return

    # Cenário B: caminho ssh-rsa
    if scenario == "ssh_rsa_path":
        dummy_public_key = object()
        def _load_ssh_public_key(_bytes):
            return dummy_public_key
        monkeypatch.setattr(algorithms, "load_ssh_public_key", _load_ssh_public_key)

        self_sim = DummySelf(NotCryptoKey)
        key = "ssh-rsa AAAAB3NzaC1yc2E..."
        result = algorithms.RSAAlgorithm.prepare_key(self_sim, key)
        assert result is dummy_public_key
        assert getattr(self_sim, "check_called_with", None) is dummy_public_key
        return

    # Cenário C: caminho PEM privado
    if scenario == "pem_private_path":
        dummy_private_key = object()
        def _load_pem_private_key(_bytes, password=None):
            return dummy_private_key
        monkeypatch.setattr(algorithms, "load_pem_private_key", _load_pem_private_key)

        self_sim = DummySelf(NotCryptoKey)
        key = "-----BEGIN PRIVATE KEY-----\n..."
        result = algorithms.RSAAlgorithm.prepare_key(self_sim, key)
        assert result is dummy_private_key
        assert getattr(self_sim, "check_called_with", None) is dummy_private_key
        return

    # Cenário D: input inválido que leva a InvalidKeyError
    if scenario == "invalid_input_raises_InvalidKeyError":
        def _raise_value_error(*args, **kwargs):
            raise ValueError()
        monkeypatch.setattr(algorithms, "load_pem_private_key", _raise_value_error)
        monkeypatch.setattr(algorithms, "load_pem_public_key", _raise_value_error)

        self_sim = DummySelf(NotCryptoKey)
        key = b"not a pem"
        with pytest.raises(algorithms.InvalidKeyError):
            algorithms.RSAAlgorithm.prepare_key(self_sim, key)
