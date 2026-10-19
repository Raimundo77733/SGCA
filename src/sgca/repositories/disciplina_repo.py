from src.sgca.errors.DatabaseErrors import NaoEncontradoError


class DisciplinaRepo:
    """Catálogo de disciplinas e seus pré-requisitos (guardados como 'A,B,C')."""

    def __init__(self, banco):
        self.banco = banco

    def inserir(self, nome, cod_curso, creditos, carga_horaria, prerequisitos=(), semestre=None):
        with self.banco.transacao():
            self.banco.executar(
                "INSERT INTO Disciplinas (nome, semestre, cod_curso, creditos, carga_horaria, "
                "prerequisitos) VALUES (?, ?, ?, ?, ?, ?)",
                (nome, semestre, cod_curso, creditos, carga_horaria, ",".join(prerequisitos)))

    def obter(self, nome):
        """Devolve a disciplina (dict) ou levanta NaoEncontradoError."""
        disciplina = self.buscar(nome)
        if disciplina is None:
            raise NaoEncontradoError(f"Disciplina {nome} não encontrada.")
        return disciplina

    def buscar(self, nome):
        linha = self.banco.fetch_one_line("SELECT * FROM Disciplinas WHERE nome = ?", (nome,))
        if linha is None:
            return None
        disciplina = dict(linha)
        return disciplina

    def listar_por_curso(self, cod_curso):
        linhas = self.banco.fetch_all_lines(
            "SELECT * FROM Disciplinas WHERE cod_curso = ? ORDER BY semestre, nome", (cod_curso,))
        disciplinas = []
        for linha in linhas:
            disciplinas.append(dict(linha))
        return disciplinas

    def requisitos(self, nome):
        """Lista de nomes de disciplinas exigidas (vazia se não há)."""
        linha = self.banco.fetch_one_line("SELECT prerequisitos FROM Disciplinas WHERE nome = ?", (nome,))
        requisitos = []
        if linha is None:
            return requisitos
        for pedaco in linha["prerequisitos"].split(","):
            if pedaco.strip():
                requisitos.append(pedaco.strip())
        return requisitos
