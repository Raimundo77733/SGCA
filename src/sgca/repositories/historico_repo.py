class HistoricoRepo:
    """Histórico acadêmico. Ainda não há classe de domínio: devolve dicionários."""

    def __init__(self, banco):
        self.banco = banco

    def registrar(self, n_matricula, nome_disciplina, nota_final, status, creditos,
                  semestre=None, data_conclusao=None):
        with self.banco.transacao():
            self.banco.executar(
                "INSERT INTO Historico (n_matricula, nome_disciplina, semestre, "
                "nota_final, status, creditos, data_conclusao) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (n_matricula, nome_disciplina, semestre, nota_final, status, creditos,
                 data_conclusao))

    def listar(self, n_matricula):
        linhas = self.banco.fetch_all_lines(
            "SELECT * FROM Historico WHERE n_matricula = ? ORDER BY semestre, nome_disciplina",
            (n_matricula,))
        historico = []
        for linha in linhas:
            historico.append(dict(linha))
        return historico

    def disciplinas_aprovadas(self, n_matricula):
        linhas = self.banco.fetch_all_lines(
            "SELECT nome_disciplina FROM Historico "
            "WHERE n_matricula = ? AND status = 'APROVADO'", (n_matricula,))
        aprovadas = set()
        for linha in linhas:
            aprovadas.add(linha["nome_disciplina"])
        return aprovadas

    def calcular_cr(self, n_matricula):
        """CR = soma(nota final x créditos) / soma(créditos), só das disciplinas aprovadas."""
        linha = self.banco.fetch_one_line(
            "SELECT SUM(nota_final * creditos) AS soma_ponderada, SUM(creditos) AS total_creditos "
            "FROM Historico WHERE n_matricula = ? AND status = 'APROVADO'",
            (n_matricula,))
        if linha["total_creditos"] is None or linha["total_creditos"] == 0:
            return 0.0
        cr = linha["soma_ponderada"] / linha["total_creditos"]
        return cr
