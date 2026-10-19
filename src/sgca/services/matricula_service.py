from datetime import date, datetime

from src.sgca.domain.Matricula import Matricula
from src.sgca.errors.Validation import ChoqueHorarioError, EstadoInvalidoError,PreRequisitoError, TurmaCheiaError,TurmaFechadaError
from src.sgca.errors.DatabaseErrors import JaExisteError
from src.sgca.errors.UnauthorizedError import PrazoTrancamentoError


class MatriculaService:
    def __init__(self, alunos, turmas, matriculas, historico, disciplinas,
                 banco, nota_minima, frequencia_minima,
                 data_limite_trancamento_turma, data_limite_trancamento_curso):
        self.alunos = alunos
        self.turmas = turmas
        self.matriculas = matriculas
        self.historico = historico
        self.disciplinas = disciplinas
        self.banco = banco
        self.nota_minima = nota_minima
        self.frequencia_minima = frequencia_minima
        self.data_limite_trancamento_turma = data_limite_trancamento_turma
        self.data_limite_trancamento_curso = data_limite_trancamento_curso

    def matricular(self, n_matricula, id_turma):
        with self.banco.transacao():
            aluno = self.alunos.obter(n_matricula)
            turma = self.turmas.obter(id_turma)

            if aluno.status_curso == "Trancado":
                raise EstadoInvalidoError("O curso do aluno está trancado; não é possível matricular.")
            if turma.status != "Aberta":
                raise TurmaFechadaError("A turma não está aberta para matrículas.")
            if self.matriculas.existe(n_matricula, id_turma):
                raise JaExisteError("O aluno já está matriculado nesta turma.")
            self._verificar_requisitos(aluno, turma)

            matricula = Matricula(turma, aluno)
            outras_turmas = self._turmas_em_andamento(aluno, turma.semestre)
            if not matricula.verificar_choque_horario(turma, outras_turmas):
                raise ChoqueHorarioError("A turma tem horário em conflito com outra turma do aluno neste semestre.")
            if not matricula.verificar_vagas(turma) or not self.turmas.reservar_vaga(id_turma):
                raise TurmaCheiaError("A turma não tem vagas disponíveis.")
            self.matriculas.inserir(matricula)
        return matricula

    def trancar_disciplina(self, n_matricula, id_turma, hoje=None):
        if hoje is None:
            hoje = date.today()
        if hoje > self.data_limite_trancamento_turma:
            limite = self.data_limite_trancamento_turma.strftime("%d/%m/%Y")
            raise PrazoTrancamentoError(f"O prazo para trancar a turma terminou em {limite}.")
        with self.banco.transacao():
            matricula = self.matriculas.obter(n_matricula, id_turma)
            if matricula.status != "Cursando":
                raise EstadoInvalidoError("Só é possível trancar uma matrícula em andamento.")
            matricula.status = "Trancada"
            self.matriculas.atualizar(matricula)
            self.turmas.liberar_vaga(id_turma)

    def trancar_curso(self, n_matricula, hoje=None):
        if hoje is None:
            hoje = date.today()
        if hoje > self.data_limite_trancamento_curso:
            limite = self.data_limite_trancamento_curso.strftime("%d/%m/%Y")
            raise PrazoTrancamentoError(f"O prazo para trancar o curso terminou em {limite}.")
        aluno = self.alunos.obter(n_matricula)
        aluno.status_curso = "Trancado"
        self.alunos.atualizar(aluno)

    def lancar_nota(self, n_matricula, id_turma, avaliacao, nota):
        with self.banco.transacao():
            matricula = self.matriculas.obter(n_matricula, id_turma)
            matricula.lancar_nota(avaliacao, nota)
            self.matriculas.atualizar(matricula)
        return matricula.media

    def lancar_frequencia(self, n_matricula, id_turma, data, presente):
        with self.banco.transacao():
            matricula = self.matriculas.obter(n_matricula, id_turma)
            matricula.lancar_frequencia(data, presente)
            self.matriculas.atualizar(matricula)
        return matricula.frequencia_media

    def concluir_disciplina(self, id_turma):
        """Encerra a turma, grava o histórico de cada aluno e atualiza o CR.
        Devolve uma lista de (n_matricula, situação).
        """
        resultados = []
        with self.banco.transacao():
            turma = self.turmas.obter(id_turma)
            if turma.status == "Encerrada":
                raise EstadoInvalidoError("A turma já foi encerrada.")

            data_conclusao = datetime.now().strftime("%Y-%m-%d")
            for matricula in self.matriculas.listar_por_turma(id_turma):
                if matricula.status != "Cursando":
                    continue
                situacao = matricula.calcular_situacao(self.nota_minima, self.frequencia_minima)
                matricula.status = "Concluida"
                self.matriculas.atualizar(matricula)
                creditos = turma.creditos
                self.historico.registrar(matricula.n_matricula, turma.nome_disciplina,
                                         matricula.media, situacao, creditos,
                                         turma.semestre, data_conclusao)

                aluno = self.alunos.obter(matricula.n_matricula)
                aluno.cr = self.historico.calcular_cr(matricula.n_matricula)
                self.alunos.atualizar(aluno)
                resultados.append((matricula.n_matricula, situacao))

            turma.status = "Encerrada"
            self.turmas.atualizar(turma)
        return resultados

    def _turmas_em_andamento(self, aluno, semestre):
        """Turmas em que o aluno está cursando no semestre informado."""
        turmas = []
        for matricula in self.matriculas.listar_por_aluno(aluno.matricula):
            if matricula.status != "Cursando":
                continue
            turma = self.turmas.obter(matricula.id_turma)
            if turma.semestre == semestre:
                turmas.append(turma)
        return turmas

    def _verificar_requisitos(self, aluno, turma):
        exigidos = self.disciplinas.requisitos(turma.nome_disciplina)
        aprovadas = self.historico.disciplinas_aprovadas(aluno.matricula)
        faltando = []
        for disciplina in exigidos:
            if disciplina not in aprovadas:
                faltando.append(disciplina)
        if faltando:
            raise PreRequisitoError("Pré-requisitos pendentes: " + ", ".join(faltando))
