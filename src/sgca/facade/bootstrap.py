import json
from datetime import datetime
from pathlib import Path

from src.sgca.facade.SGCAManager import SGCAManager
from src.sgca.repositories.aluno_repo import AlunoRepo
from src.sgca.repositories.banco import Banco
from src.sgca.repositories.curso_repo import CursoRepo
from src.sgca.repositories.disciplina_repo import DisciplinaRepo
from src.sgca.repositories.historico_repo import HistoricoRepo
from src.sgca.repositories.matricula_repo import MatriculaRepo
from src.sgca.repositories.schema import criar_tabelas
from src.sgca.repositories.turma_repo import TurmaRepo
from src.sgca.services.cadastro_service import CadastroService
from src.sgca.services.matricula_service import MatriculaService
from src.sgca.services.relatorio_service import RelatorioService


PASTA_SETTINGS = Path(__file__).resolve().parents[1] / "settings"


def carregar_settings(caminho=None):
    if caminho is None:
        caminho = PASTA_SETTINGS / "settings.json"
    with open(caminho, encoding="utf-8") as arquivo:
        settings = json.load(arquivo)
    return settings


def _texto_para_data(texto):
    data = datetime.strptime(texto, "%Y-%m-%d").date()
    return data


def criar_sgca(caminho_db, caminho_settings=None):
    settings = carregar_settings(caminho_settings)
    nota_minima = settings["nota_minima_aprovacao"]
    frequencia_minima = settings["frequencia_minima"]
    top_n = settings["top_n_alunos"]
    data_limite_trancamento_turma = _texto_para_data(settings["data_limite_trancamento_turma"])
    data_limite_trancamento_curso = _texto_para_data(settings["data_limite_trancamento_curso"])
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
