class RelatorioService:
    def __init__(self, alunos, turmas,matriculas, historico, disciplinas, top_n_padrao):
        self.alunos = alunos
        self.turmas = turmas
        self.matriculas=matriculas
        self.historico = historico
        self.disciplinas = disciplinas
        self.top_n_padrao = top_n_padrao

    def alunos_do_curso(self, cod_curso):
        return self.alunos.listar_por_curso(cod_curso)

    def disciplinas_do_curso(self, cod_curso):
        return self.disciplinas.listar_por_curso(cod_curso)

    def top_n_c(self, cod_curso, n=None):
        return self.alunos.repo_topnc(cod_curso, n or self.top_n_padrao)

    def top_n_t(self, id_turma, n=None):
        return self.matriculas.repo_topnt(id_turma, n or self.top_n_padrao)

    def historico_do_aluno(self, n_matricula):
        return self.historico.listar(n_matricula)

    def alunos_da_turma(self, id_turma):
        turma = self.turmas.obter(id_turma)
        return {
            "turma": turma,
            "alunos": self.alunos.listar_por_turma(id_turma),
            "ocupadas": turma.inscritos,
            "vagas": turma.vagas_max,
            "status": turma.status,
        }
