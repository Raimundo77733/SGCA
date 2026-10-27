import random

from src.sgca.errors.Validation import MatriculaInvalidaError, ValidationError, StuatusInvalidoError

MATRICULA_MIN = 100000
MATRICULA_MAX = 999999


class CadastroService:
    def __init__(self, alunos, cursos, turmas, disciplinas):
        self.alunos = alunos
        self.cursos = cursos
        self.turmas = turmas
        self.disciplinas = disciplinas

    '''Aluno'''
    def cadastrar_aluno(self, aluno):
        """Gera a matrícula se ainda não houver e grava. Devolve o número."""
        if aluno.matricula == 0:
            aluno.matricula = self._gerar_n_matricula()
        if not MATRICULA_MIN <= aluno.matricula <= MATRICULA_MAX:
            raise MatriculaInvalidaError(
                f"Número de matrícula inválido: deve estar entre {MATRICULA_MIN} e {MATRICULA_MAX}.")
        self.alunos.inserir(aluno)
        return aluno.matricula

    def editar_aluno(self, aluno):
        self.alunos.atualizar(aluno)

    def remover_aluno(self, n_matricula):
        self.alunos.remover(n_matricula)

    def buscar_aluno(self, n_matricula):
        return self.alunos.obter(n_matricula)

    def _gerar_n_matricula(self):
        while True:
            numero = random.randint(MATRICULA_MIN, MATRICULA_MAX)
            if not self.alunos.existe(numero):
                return numero

    '''Curso'''
    def inserir_curso(self, curso):
        self.cursos.inserir(curso)

    def editar_curso(self, curso):
        self.cursos.atualizar(curso)

    def remover_curso(self, cod_curso):
        self.cursos.remover(cod_curso)

    def listar_cursos(self):
        return self.cursos.listar()

    def buscar_curso(self, cod_curso):
        return self.cursos.obter(cod_curso)

    '''Disciplina'''
    def cadastrar_disciplina(self, nome, cod_curso, creditos, carga_horaria,
                             prerequisitos=(), semestre=None):
        """Grava a disciplina no curso. Pré-requisitos precisam existir antes (sem ciclos)."""
        if creditos <= 0 or carga_horaria <= 0:
            raise ValidationError("Créditos e carga horária devem ser maiores que zero.")
        self.cursos.obter(cod_curso)
        for prerequisito in prerequisitos:
            self.disciplinas.obter(prerequisito)
        self.disciplinas.inserir(nome, cod_curso, creditos, carga_horaria, prerequisitos, semestre)

    def buscar_disciplina(self, nome):
        return self.disciplinas.obter(nome)

    '''Turma'''
    def cadastrar_turma(self, turma):
        """Grava a turma e devolve o id gerado pelo banco."""
        self.turmas.inserir(turma)
        return turma.id_turma

    def editar_turma(self, turma):
        self.turmas.atualizar(turma)

    def remover_turma(self, id_turma):
        self.turmas.remover(id_turma)

    def buscar_turma(self, id_turma):
        return self.turmas.obter(id_turma)

    def fechar_turma(self,id_turma,status):
        status_permitido=["Aberta","Fechada"]
        if not (status in status_permitido):
            raise StuatusInvalidoError
        self.turmas.fechar_turma(id_turma,status)
