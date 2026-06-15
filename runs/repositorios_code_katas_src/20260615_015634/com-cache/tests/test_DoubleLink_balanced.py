import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

def test_balanced_empty_list_raises_value_error():
    dl = DoubleLink()
    with pytest.raises(ValueError) as excinfo:
        dl.balanced()
    assert "Cannot balance an empty list" in str(excinfo.value)

def test_balanced_first_closing_paren_returns_minus_one():
    dl = DoubleLink()
    dl.push(')')
    assert dl.balanced() == -1

def test_balanced_unmatched_open_returns_one():
    dl = DoubleLink()
    dl.push('(')
    dl.push('(')
    assert dl.balanced() == 1

def test_balanced_simple_pair_returns_minus_one():
    dl = DoubleLink()
    dl.push('(')
    dl.push(')')
    assert dl.balanced() == -1
