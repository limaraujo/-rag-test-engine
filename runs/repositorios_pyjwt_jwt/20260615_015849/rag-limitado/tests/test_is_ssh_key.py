import importlib
import pytest
from repositorios.pyjwt.jwt.utils import is_ssh_key

utils = importlib.import_module("repositorios.pyjwt.jwt.utils")
is_ssh_key = utils.is_ssh_key

# Verifica caminho feliz: key inicia com prefixo SSH configurado retorna True
@pytest.mark.parametrize("prefix,key", [
    (b"ssh-", b"ssh-key-1"),
    (b"ecdsa-", b"ecdsa-key-abc"),
])
def test_is_ssh_key_happy_path(monkeypatch, prefix, key):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (prefix,), raising=True)
    assert is_ssh_key(key) is True

# Verifica casos negativos: key não inicia com prefixo SSH configurado e casos de borda
@pytest.mark.parametrize("prefix,key,expected", [
    (b"ssh-", b"not-ssh-key", False),
    (b"ssh-", b"", False),
    (b"ssh-", b"ssh", False),
])
def test_is_ssh_key_negative_cases(monkeypatch, prefix, key, expected):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (prefix,), raising=True)
    assert is_ssh_key(key) is expected
