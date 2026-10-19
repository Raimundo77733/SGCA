
from src.sgca.domain.Aluno import Aluno
from src.sgca.repositories.base import Repositorio


class AlunoRepo(Repositorio):
    TABELA = "Aluno"
    CHAVE = ("n_matricula",)
    # JOIN com Curso porque o Aluno atual recebe `nome_curso` no construtor
    SELECT = ("SELECT a.n_matricula, a.nome, a.email, a.cod_curso, a.cr, "
              "a.status_curso, c.nome_curso FROM Aluno a "
              "JOIN Curso c ON c.cod_curso = a.cod_curso")
    CHAVE_SELECT = ("a.n_matricula",)

    def _para_linha(self,obj):
        return {
            "n_matricula": obj.matricula,
            "nome": obj.nome,
            "email": obj.email,
            "cod_curso": obj.cod_curso,
            "nome_curso": obj.nome_curso,
            "cr": obj.cr,
            "status_curso": obj.status_curso,
        }

    def _para_objeto(self,linha):
        aluno = Aluno(linha["nome"], linha["email"], linha["cod_curso"], linha["nome_curso"])
        aluno.matricula = int(linha["n_matricula"])  # coluna é TEXT; o domínio usa int
        aluno.cr = linha["cr"]
        aluno.status_curso = linha["status_curso"]
        return aluno


    def listar_por_curso(self, cod_curso):
        return self._consultar("WHERE a.cod_curso = ? ORDER BY a.nome", (cod_curso,))

    def top_n(self, cod_curso, n):
        return self._consultar(
            "WHERE a.cod_curso = ? ORDER BY a.cr DESC, a.nome LIMIT ?", (cod_curso, n))

    def listar_por_turma(self, id_turma):
        return self._consultar(
            "JOIN Matricula m ON m.n_matricula = a.n_matricula "
            "WHERE m.id_turma = ? ORDER BY a.nome", (id_turma,))

