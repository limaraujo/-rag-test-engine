import pytest
from repositorios.code_katas.src.get_grade import get_grade
# Testa faixas A/B/C/D (happy paths com cenários distintos)

# Testa A/B/C/D: cada conjunto cobre uma faixa de nota
@pytest.mark.parametrize("s1,s2,s3,expected", [
    (95, 93, 94, 'A'),  # média ~94 -> A
    (85, 82, 84, 'B'),  # média ~84 -> B
    (75, 78, 72, 'C'),  # média ~75 -> C
    (65, 60, 66, 'D'),  # média ~63.7 -> D
])
def test_get_grade_branches_happy_paths(s1, s2, s3, expected):
    # Verifica que get_grade retorna a faixa correspondente para cada média
    assert get_grade(s1, s2, s3) == expected

# Testa a faixa F: médias abaixo de 60 resultam em 'F'
@pytest.mark.parametrize("s1,s2,s3,expected", [
    (50, 55, 52, 'F'),  # média ~52.3 -> F
    (0, 0, 59, 'F'),    # média ~19.7 -> F
])
def test_get_grade_f_grade(s1, s2, s3, expected):
    # Verifica o caso de borda/F: médias menores que 60
    assert get_grade(s1, s2, s3) == expected
