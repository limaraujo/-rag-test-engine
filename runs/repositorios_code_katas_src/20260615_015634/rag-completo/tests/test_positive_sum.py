import pytest
from repositorios.code_katas.src.sum_positive import positive_sum


# Verifica soma de positivos em lista com positivos e negativos e zero
def test_positive_sum_happy_path():
    arr = [1, 2, 3, -2, -5, 0]
    assert positive_sum(arr) == 6

# Verifica comportamento com lista vazia
def test_positive_sum_empty_list():
    assert positive_sum([]) == 0

# Verifica caso com arr não vazia mas sem positivos
def test_positive_sum_no_positives():
    assert positive_sum([-1, 0, -3]) == 0

# Verifica caso com apenas um positivo
def test_positive_sum_single_positive():
    assert positive_sum([5]) == 5
