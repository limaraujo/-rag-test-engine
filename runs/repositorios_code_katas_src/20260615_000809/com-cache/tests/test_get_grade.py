import pytest
from repositorios.code_katas.src.get_grade import get_grade

# Verifica todas as faixas de nota usando limites exatos (A/B/C/D/F)
@pytest.mark.parametrize("s1,s2,s3,expected", [
    (90, 90, 90, 'A'),  # A
    (80, 80, 80, 'B'),  # B
    (70, 70, 70, 'C'),  # C
    (60, 60, 60, 'D'),  # D
    (50, 50, 50, 'F'),  # F
])
def test_get_grade_branches_limits(s1, s2, s3, expected):
    assert get_grade(s1, s2, s3) == expected
