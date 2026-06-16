import pytest
from repositorios.code_katas.src.parenthetics import Node


# Testa inicialização padrão (sem argumentos): verifica que value, next_node e previous_node são None
def test_node_init_defaults():
    node = Node()
    assert node.value is None
    assert node.next_node is None
    assert node.previous_node is None

# Testa inicialização com todos os campos fornecidos: verifica que todos são armazenados corretamente
def test_node_init_sets_all_fields():
    next_ref = object()
    prev_ref = object()
    node = Node(value=10, next_node=next_ref, previous_node=prev_ref)
    assert node.value == 10
    assert node.next_node is next_ref
    assert node.previous_node is prev_ref

# Testa inicialização com apenas o valor fornecido: verifica que os outros campos permanecem None
def test_node_init_value_only():
    node = Node(value="only_value")
    assert node.value == "only_value"
    assert node.next_node is None
    assert node.previous_node is None

# Testa inicialização com tipos diversos nos campos: verifica flexibilidade de armazenamento
def test_node_init_with_various_types():
    next_list = [1, 2, 3]
    prev_dict = {"key": "value"}
    node = Node(value=3.14, next_node=next_list, previous_node=prev_dict)
    assert node.value == 3.14
    assert node.next_node == next_list
    assert node.previous_node == prev_dict
