from unittest.mock import patch
import pytest
from repositorios.code_katas.src.forbes import oldest_youngest

# Teste: caminho feliz (happy path) com várias entradas válidas; verifica oldest e youngest corretos
def test_oldest_youngest_happy_path():
    data = {
        'billionaires': [
            {'name': 'Alice', 'age': 30, 'source': 'Tech', 'net_worth (USD)': 1_000_000},
            {'name': 'Bob', 'age': 82, 'source': 'Finance', 'net_worth (USD)': 5_000_000},
            {'name': 'Charlie', 'age': -5, 'source': 'Energy', 'net_worth (USD)': 200_000},
            {'name': 'Diana', 'age': 25, 'source': 'Retail', 'net_worth (USD)': 750_000},
            {'name': 'Eve', 'age': 70, 'source': 'Tech', 'net_worth (USD)': 3_000_000},
        ]
    }
    with patch('repositorios.code_katas.src.forbes.get_json', return_value=data):
        oldest, youngest = oldest_youngest()

    assert oldest[0] == 'Eve'
    assert oldest[1]['age'] == 70
    assert oldest[1]['industry'] == 'Tech'
    assert oldest[1]['net worth'] == 3_000_000

    assert youngest[0] == 'Diana'
    assert youngest[1]['age'] == 25
    assert youngest[1]['industry'] == 'Retail'
    assert youngest[1]['net worth'] == 750_000

# Teste: cenários com filtragem de idade (verifica filtragem de >=80 e <0)
def test_oldest_youngest_with_filtering():
    data = {
        'billionaires': [
            {'name': 'Kara', 'age': 18, 'source': 'Tech', 'net_worth (USD)': 1_000_000},
            {'name': 'Mio', 'age': 79, 'source': 'Finance', 'net_worth (USD)': 2_000_000},
            {'name': 'Nia', 'age': 0, 'source': 'Retail', 'net_worth (USD)': 500_000},
        ]
    }
    with patch('repositorios.code_katas.src.forbes.get_json', return_value=data):
        oldest, youngest = oldest_youngest()

    assert oldest[0] == 'Mio'
    assert oldest[1]['age'] == 79
    assert youngest[0] == 'Nia'
    assert youngest[1]['age'] == 0

# Teste: exceção quando nenhum item é elegível (empty age_dict)
def test_oldest_youngest_raises_on_empty():
    data = {
        'billionaires': [
            {'name': 'X', 'age': 85, 'source': 'Tech', 'net_worth (USD)': 10},
            {'name': 'Y', 'age': 90, 'source': 'Finance', 'net_worth (USD)': 20},
        ]
    }
    with patch('repositorios.code_katas.src.forbes.get_json', return_value=data):
        with pytest.raises(ValueError):
            oldest_youngest()
