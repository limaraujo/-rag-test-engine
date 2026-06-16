import pytest
from repositorios.code_katas.src.get_grade import get_grade

# Verifica as cinco faixas (A,B,C,D,F) usando cenários parametrizados para cobrir cada branch da função get_grade
@pytest.mark.parametrize("s1,s2,s3,expected", [
    (95, 92, 90, 'A'),  # A: avg >= 90
    (80, 82, 78, 'B'),  # B: 80 <= avg < 90
    (75, 70, 68, 'C'),  # C: 70 <= avg < 80
    (60, 60, 60, 'D'),  # D: 60 <= avg < 70
    (50, 50, 50, 'F'),  # F: avg < 60
])
def test_get_grade_branches(s1, s2, s3, expected):
    assert get_grade(s1, s2, s3) == expected
