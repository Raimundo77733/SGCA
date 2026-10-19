import json
from datetime import datetime

from src.sgca.domain.Turma import Turma
from src.sgca.repositories.base import Repositorio


def _data_para_texto(data):
    """Devolve 'AAAA-MM-DD' (formato ISO) para datetime, texto ISO ou texto 'dd/mm/aaaa'."""
    if hasattr(data, "strftime"):
        texto = data.strftime("%Y-%m-%d")
    elif "/" in data:
        texto = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
    else:
        texto = data
    return texto


def _texto_para_data(texto):
    return datetime.strptime(texto, "%Y-%m-%d").strftime("%d/%m/%Y")


class TurmaRepo(Repositorio):
    TABELA = "Turma"
    CHAVE = ("id_turma",)
    AUTO_INCREMENT = True
    SELECT = ("SELECT t.*,"
            "d.nome AS nome_disciplina,"
            "d.cod_curso,"
            "c.nome_curso,"
            "d.carga_horaria,"
            "d.creditos"
            " FROM Turma t"
            " JOIN Disciplinas d ON d.id = t.id_disciplina"
            " JOIN Curso c ON c.cod_curso = d.cod_curso")
    CHAVE_SELECT = ("t.id_turma",)

    def _para_linha(self, obj):
        return {
            "id_turma": obj.id_turma,
            "id_disciplina": obj.id_disciplina,
            "semestre": obj.semestre,
            "vagas_max": obj.vagas_max,
            "status": obj.status,
            "data_limite": _data_para_texto(obj.data_limite),
            "horarios": json.dumps(obj.horarios, ensure_ascii=False),
            "local": obj.local,
            "inscritos": obj.inscritos,
        }

    def _para_objeto(self, linha):
        turma = Turma(
            horarios=json.loads(linha["horarios"]),
            vagas_max=linha["vagas_max"],
            id_disciplina=linha["id_disciplina"],
            semestre=linha["semestre"],
            data_limite=_texto_para_data(linha["data_limite"]),
        )

        turma.id_turma = linha["id_turma"]
        turma.status = linha["status"]
        turma.local = linha["local"]
        turma.inscritos = linha["inscritos"]
        # dados que vêm da disciplina e do curso (JOIN)
        turma.nome_disciplina = linha["nome_disciplina"]
        turma.cod_curso = linha["cod_curso"]
        turma.nome_curso = linha["nome_curso"]
        turma.carga_horaria = linha["carga_horaria"]
        turma.creditos = linha["creditos"]
        return turma

    def _definir_chave(self, obj, valor):
        obj.id_turma = valor

    def listar_por_curso(self, cod_curso):
        return self._consultar("WHERE d.cod_curso = ? ORDER BY t.id_turma", (cod_curso,))

    def reservar_vaga(self, id_turma):
        """Utiliza uma instrução única condicional para atualizar o número de inscritos da turma,
        a fim de evitar aumentar o contador sem o cadastro por cause de erros
        """
        with self.banco.transacao():
            cursor = self.banco.executar(
                "UPDATE Turma SET inscritos = inscritos + 1 "
                "WHERE id_turma = ? AND inscritos < vagas_max", (id_turma,))
        if cursor.rowcount == 1:
            #Indica o número de linhas afetadas pela transação 1 linha= atualizada, 0= cheia, inexistente ,condição não satisfeita
            return True
        return False

    def liberar_vaga(self, id_turma):
        with self.banco.transacao():
            self.banco.executar(
                "UPDATE Turma SET inscritos = inscritos - 1 "
                "WHERE id_turma = ? AND inscritos > 0", (id_turma,))
