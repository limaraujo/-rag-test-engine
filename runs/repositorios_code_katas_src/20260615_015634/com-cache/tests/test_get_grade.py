import pytest
from repositorios.code_katas.src.get_grade import get_grade

# Verifica A: média >= 90
def test_get_grade_A():
    assert get_grade(95, 92, 90) == 'A'

# Verifica B: média entre 80 e 89
def test_get_grade_B():
    assert get_grade(80, 80, 80) == 'B'

# Verifica C: média entre 70 e 79
def test_get_grade_C():
    assert get_grade(70, 70, 71) == 'C'

# cobre ramos D e F: casos de borda (60) e falha (0)
@pytest.mark.parametrize("scores, expected", [((60, 60, 60), 'D'), ((0, 0, 0), 'F')])
def test_get_grade_D_and_F(scores, expected):
    s1, s2, s3 = scores
    assert get_grade(s1, s2, s3) == expected
