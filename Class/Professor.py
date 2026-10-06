class Professor:
    """Professores podem lançar notas, faltas e presenças"""

    def __init__(self, nome, email, identificador, lista_turmas):
        self.identificador=identificador
        self.lista_turmas = lista_turmas

    def lancar_nota(self):
        """Lança notas dos alunos"""
        pass

    def lancar_frequencia(self):
        """Lança frequência dos alunos"""
        pass

    def calcular_situacao(self):
        """Calcula a situação de cada aluno (aprovado/reprovado)"""
        pass

    def calcular_taxa_aprov(self,id_turma):
        """Calcula a taxa de aprovação da turma"""
        #lista_alunos=self.database_link.get_lista_alunos_turma(id_turma)
        #for
        #return lista_alunos
        pass

    def mostrar_distrib_notas(self):
        """Mostra a distribuição de notas da turma"""
        pass


