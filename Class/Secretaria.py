from Class.Aluno import Aluno
from database_methods import Data_link_sql

class Secretaria:
    """Secretaria pode cadastrar e modificar informações dos alunos"""

    def __init__(self, nome, email, identificador):
        self.nome=nome
        self.email=email
        self.identificador=identificador
        self._database_link=Data_link_sql()

    def cadastrar_aluno(self,aluno):
        """Cadastra um novo aluno no sistema"""
        if aluno.matricula==0:aluno.matricula=aluno.gerar_n_matricula()
        if 999999>aluno.matricula>100000:
            self._database_link.novo_aluno_database(aluno)
            return None
        else:
            return "Tentativa de cadastro com número de matrícula inválido"

    def editar_dados_aluno(self, aluno):
        """Edita os dados de um aluno"""
        self._database_link.update_aluno_database(aluno)

    def remover_aluno(self,numero_matricula):
        """Remove um aluno do sistema"""
        self._database_link.remove_aluno_database(numero_matricula)

    def get_aluno_por_matricula(self,n_matricula):
        database_line=self._database_link.get_aluno_database(n_matricula)
        aluno=Aluno(database_line[1],database_line[2],database_line[3])
        aluno.matricula=database_line[0]
        return aluno

    def listar_cursos(self):
        """Lista todos os cursos disponíveis"""
        cursos=self._database_link.get_lista_cursos_database()
        for curso in cursos:
            print(curso)

    def inserir_curso(self, curso):
        """Cria um novo curso"""
        self._database_link.insert_curso_database(curso)

    def remover_curso(self, cod_curso):
        """Remove um curso"""
        self._database_link.remove_curso_database(cod_curso)

    def editar_dados_curso(self, curso):
        """Edita os dados do curso"""
        self._database_link.update_curso_database(curso)

    def matricular(self,matricula):
        self._database_link.nova_matricula_database(matricula)
