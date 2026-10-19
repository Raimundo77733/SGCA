from src.sgca.domain.Curso import Curso
from src.sgca.repositories.base import Repositorio


class CursoRepo(Repositorio):
    TABELA = "Curso"
    CHAVE = ("cod_curso",)

    def _para_linha(self, curso):
        return {"cod_curso": curso.cod_curso, "nome_curso": curso.nome_curso}

    def _para_objeto(self, linha):
        return Curso(linha["nome_curso"], linha["cod_curso"])
