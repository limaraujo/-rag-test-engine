import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
from repositorios.pyjwt.jwt.api_jws import PyJWS

def _make_pyjws_instance(supported=None):
    inst = object.__new__(PyJWS)
    inst._supported_crit = supported if supported is not None else {"exp", "nbf", "iat"}
    return inst

# curto: caminho feliz (happy path) com extensão suportada presente no header
def test_validate_crit_happy_path():
    inst = _make_pyjws_instance({"exp", "nbf"})
    headers = {"crit": ["exp"], "exp": {"some": "value"}}
    PyJWS._validate_crit(inst, headers)  # should not raise

# curto: borda - crit não é lista ou está vazia deve levantar InvalidTokenError
@pytest.mark.parametrize("crit_value", [[], None])
def test_validate_crit_empty_or_not_list_raises(crit_value):
    inst = _make_pyjws_instance({"exp", "nbf"})
    with pytest.raises(InvalidTokenError):
        PyJWS._validate_crit(inst, {"crit": crit_value})

# curto: borda - extensões inválidas ou não suportadas levantam InvalidTokenError
@pytest.mark.parametrize("crit_value", [[1], ["unknown"]])
def test_validate_crit_invalid_exts_raises(crit_value):
    inst = _make_pyjws_instance({"exp", "nbf", "aud"})
    with pytest.raises(InvalidTokenError):
        PyJWS._validate_crit(inst, {"crit": crit_value})

# curto: borda - extensão é suportada e listada, mas está ausente no header
def test_validate_crit_missing_header_raises():
    inst = _make_pyjws_instance({"exp", "nbf"})
    with pytest.raises(InvalidTokenError):
        PyJWS._validate_crit(inst, {"crit": ["exp"]})
