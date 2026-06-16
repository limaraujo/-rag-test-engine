from models.tarefa import Tarefa

class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = []

    def adicionar(self, titulo):
        tarefa = Tarefa(titulo)
        self.tarefas.append(tarefa)
        return tarefa

    def listar_pendentes(self):
        return [t for t in self.tarefas if not t.concluida]

    def total(self):
        return len(self.tarefas)
