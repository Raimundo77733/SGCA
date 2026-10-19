from datetime import datetime

from src.sgca.errors.UnauthorizedError import EstadoMatriculaError
from src.sgca.errors.Validation import (EstadoInvalidoError, FrequenciaInvalidaError,
                                        NotaInvalidaError)


class Matricula:
    """Matricula relaciona o objeto aluno e turma para verificar os dados"""

    def __init__(self, turma, aluno):
        self.n_matricula = aluno.matricula
        self.id_turma = turma.id_turma
        self.media = 0
        self.notas = {}
        self.frequencia_media = 0
        self.registro_frequencia = {}
        self._status = "Cursando"

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self,status):
        estados_permitidos_matricula=["Cursando","Trancada","Concluida"]
        if status not in estados_permitidos_matricula:
            raise EstadoMatriculaError(f"Estado de matrícula inválido: {status}")
        self._status=status

    def verificar_vagas(self,turma):
        """Verifica se há vagas disponíveis na turma"""
        if turma.inscritos < turma.vagas_max:
            return True
        return False

    def verificar_choque_horario(self, turma, outras_turmas):
        """Devolve True se a turma NÃO tem choque com nenhuma das outras turmas"""
        for outra in outras_turmas:
            if turma.tem_choque_com(outra):
                return False
        return True

    def _verificar_cursando(self):
        if self._status != "Cursando":
            raise EstadoInvalidoError("Só é possível lançar notas e frequência em matrícula em andamento.")

    def lancar_nota(self, avaliacao, nota):
        """Registra a nota (0-10) de uma avaliação e recalcula a média"""
        self._verificar_cursando()
        try:
            nota = float(nota)
        except (TypeError, ValueError):
            raise NotaInvalidaError("A nota deve ser um número entre 0 e 10.")
        if not 0 <= nota <= 10:
            raise NotaInvalidaError("A nota deve estar entre 0 e 10.")
        self.notas[avaliacao] = nota
        soma = 0
        for valor in self.notas.values():
            soma += valor
        self.media = soma / len(self.notas)

    def lancar_frequencia(self, data, presente):
        """Registra presença (True) ou falta (False) em uma data e recalcula a frequência (0-100)"""
        self._verificar_cursando()
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except (TypeError, ValueError):
            raise FrequenciaInvalidaError("A data deve estar no formato dd/mm/aaaa.")
        if not isinstance(presente, bool):
            raise FrequenciaInvalidaError("A presença deve ser True (presente) ou False (falta).")
        self.registro_frequencia[data] = presente
        presencas = 0
        for foi in self.registro_frequencia.values():
            if foi:
                presencas += 1
        self.frequencia_media = presencas / len(self.registro_frequencia) * 100

    def calcular_situacao(self, nota_minima, frequencia_minima):
        """Situação final pela média e frequência atuais"""
        if self.media < nota_minima:
            return "REPROVADO_POR_NOTA"
        if self.frequencia_media < frequencia_minima:
            return "REPROVADO_POR_FREQUENCIA"
        return "APROVADO"
