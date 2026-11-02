from models import Repositorio
from domain import Curso


class CursoRepo(Repositorio):
    TABELA = "Curso"
    CHAVE = ("cod_curso",)

    def _para_linha(self, obj):
        return {"cod_curso": obj.cod_curso, "nome_curso": obj.nome_curso, "carga_horaria":obj.carga_horaria,"disciplinas":obj.disciplinas}

    def _para_objeto(self, linha):
        obj=Curso(linha["nome_curso"], linha["cod_curso"], linha["carga_horaria"])
        obj.disciplinas=linha["disciplinas"]
        return obj


