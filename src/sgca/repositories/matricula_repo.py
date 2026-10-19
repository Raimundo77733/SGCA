import json
from types import SimpleNamespace

from src.sgca.domain.Matricula import Matricula
from src.sgca.repositories.base import Repositorio


class MatriculaRepo(Repositorio):
    TABELA = "Matricula"
    CHAVE = ("n_matricula", "id_turma")   # chave natural: um aluno por turma

    def _para_linha(self, obj):
        return {
            "n_matricula": obj.n_matricula,
            "id_turma": obj.id_turma,
            "status": obj.status,
            "media": obj.media,
            "frequencia_media": obj.frequencia_media,
            "notas": json.dumps(obj.notas),
            "registro_frequencia": json.dumps(obj.registro_frequencia),
        }

    def _para_objeto(self, linha):
        # Matricula(turma, aluno) só lê `turma.id_turma` e `aluno.matricula`;
        # SimpleNamespace evita carregar turma e aluno inteiros só para isso.
        matricula = Matricula(SimpleNamespace(id_turma=linha["id_turma"]),
                              SimpleNamespace(matricula=int(linha["n_matricula"])))
        matricula.media = linha["media"]
        matricula.frequencia_media = linha["frequencia_media"]
        matricula.notas = json.loads(linha["notas"] or "{}")
        matricula.registro_frequencia = json.loads(linha["registro_frequencia"] or "{}")
        matricula.status = linha["status"]
        return matricula

    def listar_por_aluno(self, n_matricula):
        return self._consultar("WHERE n_matricula = ?", (n_matricula,))

    def listar_por_turma(self, id_turma):
        return self._consultar("WHERE id_turma = ?", (id_turma,))
