from database_methods import Data_link_sql
from tempo_aux import date_get, criar_data


class Turma:

    def __init__(self,cod_curso , nome_disciplina, carga_horaria,data_limite,
                 semestre, horarios, vagas_max):

        self._database_link=Data_link_sql()

        self.cod_curso = cod_curso
        self.nome_disciplina = nome_disciplina
        self.carga_horaria = carga_horaria
        self.data_limite = criar_data(data_limite)
        self.semestre = semestre
        self.horarios = horarios
        self.vagas_max = vagas_max

        self.inscritos=0

        self.id_turma =3
        self.status = "Aberta"
        self.local = ""


    def __len__(self):
        return self.inscritos

    def __str__(self):
        lista_alunos=self.listar_alunos()
        for aluno in lista_alunos:
            print(aluno)

    def cadastrar_turma(self):
        """Cadastra a turma no sistema"""
        self._database_link.nova_turma_database(self)

    def remover_turma(self):
        """Remove a turma do sistema"""
        self._database_link.remove_turma_database(self.id_turma)

    def editar_dados_turma(self):
        """Edita os dados da turma"""
        self._database_link.update_turma_database(self)

    def listar_alunos(self):
        """Lista todos os alunos matriculados"""
        lista_alunos=self._database_link.get_lista_alunos_turma(self.id_turma)
        return lista_alunos


