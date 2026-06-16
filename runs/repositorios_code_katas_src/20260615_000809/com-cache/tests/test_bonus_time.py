import pytest
from repositorios.code_katas.src.fatcat import bonus_time

# curto: cenários combinados de salary e bonus cobrindo caminho principal e ramificações
@pytest.mark.parametrize("salary, bonus, expected", [
    (1000, True, "$10000"),  # caminho feliz com bônus ativo
    (1000, False, "$1000"),  # sem bônus
    (12, 1, "$120"),         # bônus truthy não-bool
])
def test_bonus_time_various_inputs(salary, bonus, expected):
    assert bonus_time(salary, bonus) == expected

# curto: lança TypeError quando o salário não é numérico (None provoca erro na multiplicação)
def test_bonus_time_invalid_salary_raises_type_error():
    with pytest.raises(TypeError):
        bonus_time(None, True)
