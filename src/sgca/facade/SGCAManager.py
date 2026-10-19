"""Fachada: um único objeto que a CLI/API recebe.

Não tem SQL nem regra de negócio: só agrupa os serviços.
    sistema.cadastro.cadastrar_aluno(aluno)
    sistema.matricula.matricular(555555, 12)
    sistema.relatorio.top_n("SW")
"""


class SGCAManager:
    def __init__(self, cadastro, matricula, relatorio):
        self.cadastro = cadastro
        self.matricula = matricula
        self.relatorio = relatorio
