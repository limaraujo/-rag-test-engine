from dataclasses import dataclass

@dataclass
class Tarefa:
    titulo: str
    concluida: bool = False

    def concluir(self):
        self.concluida = True
