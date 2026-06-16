import pytest
from repositorios.code_katas.src.get_grade import get_grade

# Verifica todas as faixas (A/B/C/D/F) usando cenários nos limites de cada faixa
@pytest.mark.parametrize("s1,s2,s3,expected", [
    (90, 90, 90, 'A'),  # linha de corte A
    (80, 80, 80, 'B'),  # linha de corte B
    (70, 70, 70, 'C'),  # linha de corte C
    (60, 60, 60, 'D'),  # linha de corte D
    (0, 0, 0, 'F'),     # falha total
])
def test_get_grade_branches(s1, s2, s3, expected):
    assert get_grade(s1, s2, s3) == expected
