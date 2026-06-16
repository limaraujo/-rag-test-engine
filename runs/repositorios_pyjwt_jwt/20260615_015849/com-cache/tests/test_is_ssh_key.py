import pytest
import repositorios.pyjwt.jwt.utils as utils
from repositorios.pyjwt.jwt.utils import is_ssh_key


# Verifica caminho feliz (happy path) com formato SSH forçado via monkeypatch
def test_is_ssh_key_happy_path(monkeypatch):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (b"ssh-",), raising=False)
    assert is_ssh_key(b"ssh-rsa AAAAB3NzaC1yc2E") is True


# Verifica o caso negativo onde o key não começa com o formato SSH
def test_is_ssh_key_negative_path(monkeypatch):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (b"ssh-",), raising=False)
    assert is_ssh_key(b"not-a-ssh-key") is False


# Verifica caso de borda: input vazio não é reconhecido como SSH key
def test_is_ssh_key_empty_input(monkeypatch):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (b"ssh-",), raising=False)
    assert is_ssh_key(b"") is False


# Verifica compatibilidade de tipo: input pode ser bytearray
def test_is_ssh_key_bytearray_input(monkeypatch):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (b"ssh-",), raising=False)
    assert is_ssh_key(bytearray(b"ssh-key-xyz")) is True
