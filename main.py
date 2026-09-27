class Oferta:
    pass
class Pessoa:
    pass

class Turma(Oferta):
    '''Turma armazena as disciplinas disponíveis, com lista de aluno, definição do status e tempo.'''
    def __init__(self,curso, id_turma,aluno, disciplina,prerequisitos, carga_horaria, semestre, horarios, vagas_max, local,
                 tempo_limite_matricula,ementa):
        self.curso=curso
        self.id_turma=id_turma
        self.lista_alunos = []
        self.semestre=semestre
        self.horarios=horarios
        self.vagas_max=vagas_max
        self.disciplina=disciplina
        self.prerequisitos=prerequisitos
        self.status = "Aberta"
        self.carga_horaria=carga_horaria
        self.tempo_limite_matricula=tempo_limite_matricula
        self.local=local
        self.ementa=ementa

    def cadastrar_turma(self):pass
    def remover_turma(self):pass
    def editar_dados_turma(self):pass
    def listar_alunos(self):pass
    def calcular_taxa_aprov(self):pass
    def mostrar_distrib_notas(self):pass



class Aluno(Pessoa):
    '''Aluno armazena listas de matriculas ativas, concluidas e  histórico'''
    def __init__(self, nome, email,cod_curso, n_matricula,historico):
        self.n_matricula=n_matricula
        self.historico=historico
        self.matriculas_ativas=[]
        self.matriculas_concluidas=[]
        self.cod_curso=cod_curso

    def calcular_cr(self):pass
    def mostrar_historico(self):pass
    def trancar_curso(self):pass
    def trancar_disciplina(self):pass


class Secretaria(Pessoa):
    '''Secretaria pode cadastrar e modificar informações dos alunos'''
    def cadastrar_aluno(self): pass

    def editar_dados_aluno(self):pass

    def remover_aluno(self): pass


class Professor(Pessoa):
    '''Professores podem lançar notas, faltas e presenças'''
    def __init__(self, nome, email, identificador,lista_turmas):
        super().__init__(nome, email, identificador)
        self.lista_turmas=lista_turmas

    def lancar_nota(self): pass

    def lancar_frequencia(self): pass

    def calcular_situacao(self):pass

class Curso:
    '''Curso armazena a lista dos alunos que estão no curso e as disciplinas'''
    def __init__(self, nome_curso, cod_curso, disciplinas_do_curso,aluno):
        self.lista_alunos = []
        self.nome_curso=nome_curso
        self.cod_curso=cod_curso
        self.disciplinas_do_curso=disciplinas_do_curso
    def listar_cursos(self):pass
    def criar_curso(self):pass
    def remover_curso(self):pass
    def editar_dados_curso(self):pass
    def relatorio_topn(self):pass
    def relatorio_risco(self):pass


class Matricula:
    '''Matricula relaciona o objeto aluno e turma para verificar os dados'''
    def __init__(self, aluno,turma):
        self.aluno = aluno
        self.turma=turma
        self.media = 0
        self.notas=[]
        self.frequencia_media = 0
        self.registro_frequencia=[]
        self.status = "Cursando"
        self.tempo_restante_trancamento=0

    def verificar_requisitos(self):pass
    def verificar_vagas(self):pass
    def verificar_choque_horario(self):pass