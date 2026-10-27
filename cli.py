import argparse

from src.sgca.domain.Aluno import Aluno
from src.sgca.domain.Curso import Curso
from src.sgca.domain.Turma import Turma
from src.sgca.errors.DatabaseErrors import DatabaseErrors
from src.sgca.errors.UnauthorizedError import UnauthorizedError
from src.sgca.errors.Validation import ValidationError
from src.sgca.facade.bootstrap import criar_sgca


# ============================================================================
# AÇÕES: cada função faz uma coisa e recebe o sistema e os argumentos da CLI
# ============================================================================

# --- cursos -----------------------------------------------------------------
def adicionar_curso(sistema, args):
    curso = Curso(args.nome_curso, args.cod_curso)
    sistema.cadastro.inserir_curso(curso)
    print(f"Curso {curso.nome_curso} ({curso.cod_curso}) criado")


def remover_curso(sistema, args):
    sistema.cadastro.remover_curso(args.cod_curso)
    print(f"Curso {args.cod_curso} removido")


def listar_cursos(sistema, args):
    cursos = sistema.cadastro.listar_cursos()
    for curso in cursos:
        print(f"{curso.cod_curso} - {curso.nome_curso}")


# --- alunos -----------------------------------------------------------------
def cadastrar_aluno(sistema, args):
    curso = sistema.cadastro.buscar_curso(args.cod_curso)
    aluno = Aluno(args.nome, args.email, curso.cod_curso, curso.nome_curso)
    n_matricula = sistema.cadastro.cadastrar_aluno(aluno)
    print(f"Criando {aluno.nome} ({n_matricula})")


def editar_aluno(sistema, args):
    aluno = sistema.cadastro.buscar_aluno(args.matricula)
    if args.nome:
        aluno.nome = args.nome
    if args.email:
        aluno.email = args.email
    sistema.cadastro.editar_aluno(aluno)
    print(f"Aluno {args.matricula} atualizado")


def remover_aluno(sistema, args):
    sistema.cadastro.remover_aluno(args.matricula)
    print(f"Aluno {args.matricula} removido")


def buscar_aluno(sistema, args):
    aluno = sistema.cadastro.buscar_aluno(args.matricula)
    print(aluno)


# --- turmas -----------------------------------------------------------------
def cadastrar_turma(sistema, args):
    disciplina = sistema.cadastro.buscar_disciplina(args.disciplina)

    # os horários viram um dicionário: {"1": "SEG 08:00", "2": "QUA 10:00"}
    horarios = {}
    numero = 1
    if args.horario:
        for horario in args.horario:
            horarios[str(numero)] = horario
            numero += 1

    turma = Turma(horarios, args.vagas_max, disciplina["id"], args.semestre, args.data_limite)
    turma.local = args.local
    id_turma = sistema.cadastro.cadastrar_turma(turma)
    print(f"Turma {id_turma} criada")


def adicionar_disciplina(sistema, args):
    sistema.cadastro.cadastrar_disciplina(args.nome, args.cod_curso, args.creditos,
                                          args.carga_horaria, args.prereq or [], args.semestre)
    print(f"Disciplina {args.nome} cadastrada no curso {args.cod_curso}")


def remover_turma(sistema, args):
    sistema.cadastro.remover_turma(args.id_turma)
    print(f"Turma {args.id_turma} removida")


def buscar_turma(sistema, args):
    turma = sistema.cadastro.buscar_turma(args.id_turma)
    print(turma)

def fechar_turma(sistema,args):
    sistema.cadastro.fechar_turma(args.id_turma, args.status)
    print(f"Status da turma: {args.id_turma} alterado para {args.status}")
# --- matrículas -------------------------------------------------------------
def matricular_aluno(sistema, args):
    sistema.matricula.matricular(args.matricula, args.id_turma)
    print(f"Aluno {args.matricula} matriculado na turma {args.id_turma}")


def trancar_disciplina(sistema, args):
    sistema.matricula.trancar_disciplina(args.matricula, args.id_turma)
    print(f"Matrícula do aluno {args.matricula} trancada na turma {args.id_turma}")


def trancar_curso(sistema, args):
    sistema.matricula.trancar_curso(args.matricula)
    print(f"Curso do aluno {args.matricula} trancado")


def lancar_nota(sistema, args):
    media = sistema.matricula.lancar_nota(args.matricula, args.id_turma, args.avaliacao, args.nota)
    print(f"Nota lançada. Média atual: {media:.2f}")


def lancar_frequencia(sistema, args):
    presente = args.presenca == "presente"
    frequencia = sistema.matricula.lancar_frequencia(args.matricula, args.id_turma, args.data, presente)
    print(f"Frequência lançada. Frequência atual: {frequencia:.1f}%")


def concluir_disciplina(sistema, args):
    resultados = sistema.matricula.concluir_disciplina(args.id_turma)
    print(f"Turma {args.id_turma} encerrada")
    for n_matricula, situacao in resultados:
        print(f"{n_matricula}: {situacao}")


#Cria todos os parsers, e retorna o principal(parser)
#requer o argumento comando para ser executado então sem comandos gera um erro
#utiliza acad como nas especificações ex: python cli.py acad add_aluno ...
def criar_parser():
    parser = argparse.ArgumentParser(prog="sgca")
    parser.add_argument("--db", default="data/sgca.db", help="Caminho do banco SQLite")
    comando = parser.add_subparsers(dest="comando", required=True)

    acad_parser = comando.add_parser("acad", help="Ações acadêmicas")
    acad_comandos = acad_parser.add_subparsers(dest="acad", required=True)

    # --- cursos ---
    add_curso = acad_comandos.add_parser("add_curso", help="Cria um novo curso")
    add_curso.add_argument("cod_curso", help="Código do curso (1000-9999)")
    add_curso.add_argument("nome_curso", help="Nome do curso")

    del_curso = acad_comandos.add_parser("del_curso", help="Remove um curso")
    del_curso.add_argument("cod_curso", help="Código do curso")

    acad_comandos.add_parser("list_cursos", help="Lista os cursos")

    # --- alunos ---
    add_aluno = acad_comandos.add_parser("add_aluno", help="Cria um novo aluno")
    add_aluno.add_argument("nome", help="Nome do aluno")
    add_aluno.add_argument("email", help="E-mail do aluno")
    add_aluno.add_argument("cod_curso", help="Código do curso")

    edit_aluno = acad_comandos.add_parser("edit_aluno", help="Edita os dados de um aluno")
    edit_aluno.add_argument("matricula", type=int, help="Número de matrícula")
    edit_aluno.add_argument("--nome", help="Novo nome")
    edit_aluno.add_argument("--email", help="Novo e-mail")

    del_aluno = acad_comandos.add_parser("del_aluno", help="Remove um aluno")
    del_aluno.add_argument("matricula", type=int, help="Número de matrícula")

    busc_aluno = acad_comandos.add_parser("busc_aluno", help="Busca um aluno pela matrícula")
    busc_aluno.add_argument("matricula", type=int, help="Número de matrícula")

    # --- turmas ---
    add_turma = acad_comandos.add_parser("add_turma", help="Cria uma nova turma")
    add_turma.add_argument("disciplina", help="Nome da disciplina")
    add_turma.add_argument("semestre", help="Semestre (ex.: 2026.2)")
    add_turma.add_argument("vagas_max", type=int, help="Número máximo de vagas")
    add_turma.add_argument("data_limite", help="Data limite de matrícula (dd/mm/aaaa)")
    add_turma.add_argument("--horario", action="append", help="Horário (pode repetir)")
    add_turma.add_argument("--local", default="", help="Local da turma")

    add_disc = acad_comandos.add_parser("add_disciplina", help="Cria uma disciplina no curso")
    add_disc.add_argument("cod_curso", help="Código do curso")
    add_disc.add_argument("nome", help="Nome da disciplina")
    add_disc.add_argument("creditos", type=float, help="Créditos da disciplina")
    add_disc.add_argument("carga_horaria", type=int, help="Carga horária")
    add_disc.add_argument("--prereq", action="append", help="Pré-requisito (nome; pode repetir)")
    add_disc.add_argument("--semestre", type=int, help="Semestre sugerido no curso")

    del_turma = acad_comandos.add_parser("del_turma", help="Remove uma turma")
    del_turma.add_argument("id_turma", type=int, help="ID da turma")

    busc_turma = acad_comandos.add_parser("busc_turma", help="Busca uma turma pelo ID")
    busc_turma.add_argument("id_turma", type=int, help="ID da turma")

    fechar_turm=acad_comandos.add_parser("fechar_turma", help="Altera o status da turma pelo ID")
    fechar_turm.add_argument("id_turma", type=int, help="ID da turma")
    fechar_turm.add_argument("status", help="ID da turma")

    # --- matrículas ---
    matricular = acad_comandos.add_parser("matricular", help="Matricula um aluno em uma turma")
    matricular.add_argument("matricula", type=int, help="Número de matrícula")
    matricular.add_argument("id_turma", type=int, help="ID da turma")

    tranc_disc = acad_comandos.add_parser("trancar_disciplina", help="Tranca a matrícula em uma turma")
    tranc_disc.add_argument("matricula", type=int, help="Número de matrícula")
    tranc_disc.add_argument("id_turma", type=int, help="ID da turma")

    tranc_curso = acad_comandos.add_parser("trancar_curso", help="Tranca o curso do aluno")
    tranc_curso.add_argument("matricula", type=int, help="Número de matrícula")

    lanc_nota = acad_comandos.add_parser("lancar_nota", help="Lança a nota de uma avaliação (0-10)")
    lanc_nota.add_argument("matricula", type=int, help="Número de matrícula")
    lanc_nota.add_argument("id_turma", type=int, help="ID da turma")
    lanc_nota.add_argument("avaliacao", help="Nome da avaliação (ex.: AB1)")
    lanc_nota.add_argument("nota", type=float, help="Nota de 0 a 10")

    lanc_freq = acad_comandos.add_parser("lancar_frequencia", help="Lança presença ou falta em uma data")
    lanc_freq.add_argument("matricula", type=int, help="Número de matrícula")
    lanc_freq.add_argument("id_turma", type=int, help="ID da turma")
    lanc_freq.add_argument("data", help="Data da aula (dd/mm/aaaa)")
    lanc_freq.add_argument("presenca", choices=["presente", "falta"], help="presente ou falta")

    concluir = acad_comandos.add_parser("concluir_disciplina", help="Encerra a turma e grava o histórico dos alunos")
    concluir.add_argument("id_turma", type=int, help="ID da turma")

    return parser



def executar(sistema, args):
    #Filtra os comandos primeiro com o acad e depois o tipo e chama a função
    if args.comando == "acad":

        if args.acad == "add_curso":
            adicionar_curso(sistema, args)
        elif args.acad == "del_curso":
            remover_curso(sistema, args)
        elif args.acad == "list_cursos":
            listar_cursos(sistema, args)

        elif args.acad == "add_aluno":
            cadastrar_aluno(sistema, args)
        elif args.acad == "edit_aluno":
            editar_aluno(sistema, args)
        elif args.acad == "del_aluno":
            remover_aluno(sistema, args)
        elif args.acad == "busc_aluno":
            buscar_aluno(sistema, args)

        elif args.acad == "add_turma":
            cadastrar_turma(sistema, args)
        elif args.acad == "add_disciplina":
            adicionar_disciplina(sistema, args)
        elif args.acad == "del_turma":
            remover_turma(sistema, args)
        elif args.acad == "busc_turma":
            buscar_turma(sistema, args)
        elif args.acad=="fechar_turma":
            fechar_turma(sistema,args)

        elif args.acad == "matricular":
            matricular_aluno(sistema, args)
        elif args.acad == "trancar_disciplina":
            trancar_disciplina(sistema, args)
        elif args.acad == "trancar_curso":
            trancar_curso(sistema, args)
        elif args.acad == "lancar_nota":
            lancar_nota(sistema, args)
        elif args.acad == "lancar_frequencia":
            lancar_frequencia(sistema, args)
        elif args.acad == "concluir_disciplina":
            concluir_disciplina(sistema, args)


def main():
    parser = criar_parser()
    args = parser.parse_args()
    sistema = criar_sgca(args.db)
    #Liga o bootstrap com a classe SGCA Manager
    try:
        executar(sistema, args)
    except (DatabaseErrors, UnauthorizedError, ValidationError) as erro:
        print(f"Erro: {erro}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
