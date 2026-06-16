import repositorios.pyjwt.jwt.utils as utils
from repositorios.pyjwt.jwt.utils import is_ssh_key

# Verifica caminho feliz: key começa com um formato SSH reconhecido
def test_is_ssh_key_happy_path():
    prefix = utils._SSH_KEY_FORMATS[0]
    key = prefix + b'some-data'
    assert is_ssh_key(key) is True

# Verifica caminho negativo: key não começa com nenhum formato SSH
def test_is_ssh_key_negative_path():
    key = b'not-a-valid-ssh-key'
    assert is_ssh_key(key) is False

# Verifica borda: key vazia não é reconhecida como SSH
def test_is_ssh_key_empty_key():
    key = b''
    assert is_ssh_key(key) is False
