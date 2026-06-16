import pytest
from unittest.mock import patch
from repositorios.code_katas.src.forbes import oldest_youngest

# verifica caminho feliz com várias idades válidas e algumas inválidas
def test_oldest_youngest_happy_path():
    data = {
        "billionaires": [
            {"name": "Alice", "age": 25, "source": "Tech", "net_worth (USD)": 1000},
            {"name": "Bob", "age": 70, "source": "Finance", "net_worth (USD)": 2000},
            {"name": "Carol", "age": 55, "source": "Retail", "net_worth (USD)": 1500},
            {"name": "Dave", "age": 30, "source": "Energy", "net_worth (USD)": 800},
            {"name": "Eve", "age": 80, "source": "Tech", "net_worth (USD)": 5000},
            {"name": "Frank", "age": -5, "source": "Tech", "net_worth (USD)": 600},
        ]
    }
    with patch('repositorios.code_katas.src.forbes.get_json', return_value=data):
        oldest, youngest = oldest_youngest()
        assert oldest[0] == "Bob"
        assert oldest[1]["age"] == 70
        assert oldest[1]["industry"] == "Finance"
        assert youngest[0] == "Alice"
        assert youngest[1]["age"] == 25

# verifica comportamento com apenas um item válido (ambos oldest/youngest são o mesmo)
def test_oldest_youngest_only_one_valid():
    data = {
        "billionaires": [
            {"name": "OnlyOne", "age": 40, "source": "Tech", "net_worth (USD)": 300}
        ]
    }
    with patch('repositorios.code_katas.src.forbes.get_json', return_value=data):
        oldest, youngest = oldest_youngest()
        assert oldest == ( "OnlyOne", {"age": 40, "industry": "Tech", "net worth": 300} )
        assert youngest == ( "OnlyOne", {"age": 40, "industry": "Tech", "net worth": 300} )

# verifica exceção quando não há itens válidos (empty age_dict)
def test_oldest_youngest_no_valid_items_raises():
    data = {
        "billionaires": [
            {"name": "X", "age": 80, "source": "X", "net_worth (USD)": 1000},
            {"name": "Y", "age": -1, "source": "Y", "net_worth (USD)": 2000}
        ]
    }
    with patch('repositorios.code_katas.src.forbes.get_json', return_value=data):
        with pytest.raises(ValueError):
            oldest_youngest()

# verifica inclusão de extremos 0 e 79 e exclusão de inválidos (>=80)
def test_oldest_youngest_extremos_e_invalidos():
    data = {
        "billionaires": [
            {"name": "Zero", "age": 0, "source": "A", "net_worth (USD)": 100},
            {"name": "SeventyNine", "age": 79, "source": "B", "net_worth (USD)": 500},
            {"name": "InvalidHigh", "age": 80, "source": "C", "net_worth (USD)": 1000}
        ]
    }
    with patch('repositorios.code_katas.src.forbes.get_json', return_value=data):
        oldest, youngest = oldest_youngest()
        assert oldest[0] == "SeventyNine"
        assert oldest[1]["age"] == 79
        assert youngest[0] == "Zero"
        assert youngest[1]["age"] == 0
