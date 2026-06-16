import pytest
from repositorios.code_katas.src.get_grade import get_grade

# verifica faixas de nota (A/B/C/D/F) com cenários cobrindo limites
@pytest.mark.parametrize("s1,s2,s3,expected", [
    (95, 92, 94, 'A'),  # A: média > 90
    (80, 80, 80, 'B'),  # B: média 80-89
    (70, 70, 70, 'C'),  # C: média 70-79
    (65, 65, 65, 'D'),  # D: média 60-69
    (50, 50, 50, 'F'),  # F: média < 60
])
def test_get_grade_variants(s1, s2, s3, expected):
    assert get_grade(s1, s2, s3) == expected
