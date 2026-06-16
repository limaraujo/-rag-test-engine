import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS


# Verifica chaves e valores padrão (caminho feliz)
def test_get_default_options_has_expected_keys_and_values():
    opts = PyJWS._get_default_options()
    assert isinstance(opts, dict)
    assert opts.get("verify_signature") is True
    assert opts.get("enforce_minimum_key_length") is False
    assert len(opts) == 2

# Verifica que cada chamada retorna um dicionário novo (isolamento de alterações)
def test_get_default_options_returns_fresh_dict_each_call():
    first = PyJWS._get_default_options()
    first["verify_signature"] = False
    second = PyJWS._get_default_options()
    assert isinstance(second, dict)
    assert second.get("verify_signature") is True
    # Garantir que alterações não afetam chamadas subsequentes
    assert first.get("verify_signature") is False
