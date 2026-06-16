import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

import pytest

# curto: happy path quando todos os claims obrigatórios estão presentes

from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

class _DummyPyJWT(PyJWT):
    def __init__(self):
        # não inicializa o ativo interno de PyJWT; apenas para isolar o método em teste
        pass

def _inst():
    return _DummyPyJWT()

def test_happy_path_all_claims_present():
    instance = _inst()
    payload = {"sub": "alice", "exp": 1700000000}
    claims = ["sub", "exp"]
    # não deve levantar nenhuma exceção
    instance._validate_required_claims(payload, claims)

# curto: lança MissingRequiredClaimError quando um claim obrigatório está ausente
def test_missing_required_claim_raises():
    instance = _inst()
    payload = {"sub": "alice"}  # "exp" ausente
    claims = ["sub", "exp"]
    with pytest.raises(MissingRequiredClaimError) as exc:
        instance._validate_required_claims(payload, claims)
    assert "exp" in str(exc.value)

# curto: ordem de verificação---primeiro claim ausente entre múltiplos é o citado no erro
def test_first_missing_among_multiple_claims_raises_first():
    instance = _inst()
    payload = {"sub": None, "exp": 123}
    claims = ["sub", "exp"]
    with pytest.raises(MissingRequiredClaimError) as exc:
        instance._validate_required_claims(payload, claims)
    assert "sub" in str(exc.value)
