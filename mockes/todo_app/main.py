from services.gerenciador import GerenciadorTarefas

def exemplo_uso():
    gestor = GerenciadorTarefas()

    gestor.adicionar("Criar testes unitários")
    gestor.adicionar("Validar cobertura")

    gestor.tarefas[0].concluir()

    print("Total:", gestor.total())
    print("Pendentes:", len(gestor.listar_pendentes()))

if __name__ == "__main__":
    exemplo_uso()
