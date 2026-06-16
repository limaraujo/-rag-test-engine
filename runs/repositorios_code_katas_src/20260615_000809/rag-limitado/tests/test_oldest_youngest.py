import pytest
from unittest.mock import patch
from repositorios.code_katas.src.forbes import oldest_youngest

# Teste: caminho feliz com dados mistos (válidos e inválidos) para oldest_youngest
@patch("repositorios.code_katas.src.forbes.get_json")
def test_oldest_youngest_basic(mock_get_json):
    mock_get_json.return_value = {
        "billionaires": [
            {"name": "Alice", "age": 30, "source": "Tech", "net_worth (USD)": 400},
            {"name": "Bob", "age": 70, "source": "Finance", "net_worth (USD)": 800},
            {"name": "Carol", "age": 50, "source": "Retail", "net_worth (USD)": 600},
            {"name": "Dan", "age": -5, "source": "Other", "net_worth (USD)": 5},
            {"name": "Eve", "age": 79, "source": "Tech", "net_worth (USD)": 1000},
            {"name": "Frank", "age": 80, "source": "Tech", "net_worth (USD)": 1200}
        ]
    }
    oldest, youngest = oldest_youngest()
    assert oldest[0] == "Eve"
    assert oldest[1]["age"] == 79
    assert youngest[0] == "Alice"
    assert youngest[1]["age"] == 30

# Teste: caso com apenas um valor válido (youngest e oldest devem ser igual)
@patch("repositorios.code_katas.src.forbes.get_json")
def test_oldest_youngest_single_valid(mock_get_json):
    mock_get_json.return_value = {
        "billionaires": [
            {"name": "OnlyOne", "age": 25, "source": "Tech", "net_worth (USD)": 42},
            {"name": "TooOld", "age": 85, "source": "Tech", "net_worth (USD)": 999}
        ]
    }
    oldest, youngest = oldest_youngest()
    assert oldest == youngest
    assert oldest[0] == "OnlyOne"
    assert oldest[1]["age"] == 25

# Teste: exceção quando não há idades válidas (empty age_dict)
@patch("repositorios.code_katas.src.forbes.get_json")
def test_oldest_youngest_no_valid_ages_raises(mock_get_json):
    mock_get_json.return_value = {
        "billionaires": [
            {"name": "A", "age": 85, "source": "Tech", "net_worth (USD)": 100},
            {"name": "B", "age": -1, "source": "Tech", "net_worth (USD)": 50}
        ]
    }
    with pytest.raises(ValueError):
        oldest_youngest()
