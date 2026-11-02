from facades.SGCAManager import SGCAManager
from models import Banco, criar_tabelas
from repositories import AlunoRepo, CursoRepo, DisciplinaRepo, HistoricoRepo, MatriculaRepo, TurmaRepo
from services import CadastroService, MatriculaService, RelatorioService
from utils import carregar_settings, texto_para_data_load_settings


def criar_sgca(caminho_db, caminho_settings=None):
    settings = carregar_settings(caminho_settings)
    nota_minima = settings["nota_minima_aprovacao"]
    frequencia_minima = settings["frequencia_minima"]
    top_n = settings["top_n_alunos"]
    data_limite_trancamento_turma = texto_para_data_load_settings(settings["data_limite_trancamento_turma"])
    data_limite_trancamento_curso = texto_para_data_load_settings(settings["data_limite_trancamento_curso"])
    #recebe todos os serviços e bancos
    banco = Banco(caminho_db)
    criar_tabelas(banco)

    alunos = AlunoRepo(banco)
    cursos = CursoRepo(banco)
    turmas = TurmaRepo(banco)
    matriculas = MatriculaRepo(banco)
    historico = HistoricoRepo(banco)
    disciplinas = DisciplinaRepo(banco)

    return SGCAManager(
        #Retorna a instância que gerencia a conexão cli->repo->banco
        cadastro=CadastroService(alunos, cursos, turmas, disciplinas),
        matricula=MatriculaService(alunos, turmas, matriculas, historico, disciplinas,
                           banco, nota_minima, frequencia_minima,
                           data_limite_trancamento_turma, data_limite_trancamento_curso),
        relatorio=RelatorioService(alunos, turmas, historico, disciplinas, top_n),
    )
