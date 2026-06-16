import pytest
from repositorios.code_katas.src.get_grade import get_grade

# Verifica emissão correta de letras para cenários: A (caminho principal), B, C, D e F (bordas)
@pytest.mark.parametrize("s1,s2,s3,expected", [
    (90, 90, 90, 'A'),  # caminho principal
    (80, 80, 80, 'B'),  # limite de B
    (70, 70, 70, 'C'),  # limite de C
    (60, 60, 60, 'D'),  # limite de D
    (50, 50, 50, 'F'),  # borda de F
])
def test_get_grade_various_branches(s1, s2, s3, expected):
    assert get_grade(s1, s2, s3) == expected
