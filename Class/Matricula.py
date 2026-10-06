from Class.Aluno import Aluno
from database_methods import Data_link_sql


class Matricula:
    """Matricula relaciona o objeto aluno e turma para verificar os dados"""

    def __init__(self, turma, aluno):
        self._database_link=Data_link_sql()

        self.n_matricula = aluno.matricula
        self.id_turma = turma.id_turma
        self.media = 0
        self.notas = []
        self.frequencia_media = 0
        self.registro_frequencia = []
        self._status = "Cursando"

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self,novo_estado):
        estados_permitidos_matricula=["Cursando","Trancada"]
        if self._status in estados_permitidos_matricula:
            self._status=novo_estado
        else:
            print("Estado não permitido")

    def verificar_requisitos(self,turma,aluno):
        """Verifica se o aluno atende aos pré-requisitos da disciplina"""
        prerequisitos=self._database_link.get_requisitos_disciplina_database(turma.nome_disciplina)
        if not prerequisitos: return True
        else:
            prerequisitos=str(prerequisitos).split(",")
            historico=self._database_link.get_historico_database(aluno.matricula)
            prerequisitos_necessarios=len(prerequisitos)
            prerequisitos_concluidos=0
            for prerequisito in prerequisitos:
                if prerequisito in historico:
                    prerequisitos_concluidos+=1
            if prerequisitos_concluidos==prerequisitos_necessarios:
                return True
            return False


    def verificar_vagas(self,turma):
        """Verifica se há vagas disponíveis na turma"""
        if turma.inscritos<turma.vagas_max:return True
        return False

    def verificar_choque_horario(self):
        """Verifica se há conflito de horários com outras disciplinas"""

        pass

