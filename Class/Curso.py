from database_methods import Data_link_sql


class Curso:
    """Curso armazena a lista dos alunos e as disciplinas do curso"""

    def __init__(self,nome_curso,cod_curso):
        self.nome_curso = nome_curso
        self.cod_curso = cod_curso
        self._database_link=Data_link_sql()
        self.disciplinas=self._database_link.get_disciplinas_do_curso_database(cod_curso)
    def __str__(self):
        lista_alunos = self.lista_alunos_curso(self.cod_curso)
        for aluno in lista_alunos:
            print(aluno)
    def lista_alunos_curso(self,cod_curso):
        lista_alunos=self._database_link.lista_alunos_curso_database(cod_curso)
        return lista_alunos

    def get_disciplinas_do_curso(self):
        disciplinas_do_curso = self._database_link.get_disciplinas_do_curso_database(self.cod_curso)
        return disciplinas_do_curso

    def relatorio_topn(self):
        """Gera relatório dos top N alunos"""
        lista_topn=self._database_link.get_topn_database(self.cod_curso)
        return lista_topn



