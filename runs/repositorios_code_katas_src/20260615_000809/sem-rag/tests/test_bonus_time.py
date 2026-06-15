import pytest
from repositorios.code_katas.src.fatcat import bonus_time


# teste: caminho feliz quando bonus é truthy
def test_bonus_time_with_bonus_true():
    assert bonus_time(1000, True) == "$10000"

# teste: sem bônus (bonus falsy)
def test_bonus_time_without_bonus_false():
    assert bonus_time(1000, False) == "$1000"

# teste: bonus é valor truthy não-bool (ex.: 1)
def test_bonus_time_with_non_boolean_truthy_bonus():
    assert bonus_time(50, 1) == "$500"

# teste: salário negativo com bônus ativo
def test_bonus_time_with_negative_salary_and_bonus():
    assert bonus_time(-100, True) == "$-1000"
