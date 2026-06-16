from mockes.todo_app.models.tarefa import Tarefa


def test_concluir_happy_path():
    """Valida que concluir marca a tarefa como concluída no caminho feliz."""
    t = Tarefa("Implementar testes com pytest")
    assert t.concluida is False
    t.concluir()
    assert t.concluida is True


def test_concluir_idempotent_when_already_true():
    """Valida que chamar concluir repetidamente não altera o estado se já estiver concluída."""
    t = Tarefa("Revisar PR")
    t.concluir()
    assert t.concluida is True
    t.concluir()
    assert t.concluida is True


def test_concluir_preserves_title_and_sets_true():
    """Valida que concluir não altera o título e marca a tarefa como concluída."""
    t = Tarefa("Documentar API")
    old_title = t.titulo
    t.concluir()
    assert t.titulo == old_title
    assert t.concluida is True


def test_concluir_when_initially_false_then_true():
    """Valida o caminho de borda: concluir quando inicialmente não concluída funciona e mantém o título."""
    t = Tarefa("Planejar sprint")
    assert t.concluida is False
    t.concluir()
    assert t.concluida is True
    assert t.titulo == "Planejar sprint"
