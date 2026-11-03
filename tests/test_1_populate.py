# test_popular_database.py
import pytest

from helpers import assert_ok, extrair_matricula, run_cli


# ---------------------------------------------------------------------------
# Dados
# ---------------------------------------------------------------------------

CURSOS = [
    (1001, "Ciência da Computação",3600),
    (1002, "Matemática",3600),
    (1003, "Engenharia Civil",3600),
    (1004, "Biologia",3600),
    (1005, "História",3600),
    (1006, "Física",3600),
]

DISCIPLINAS = [
    (1006, "Física", 3, 50, []),
    (1002, "Matemática", 3, 50, []),
    (1001, "Fundamentos de Programação", 4, 60, ["--prereq", "Matemática"]),
    (1001, "Estrutura de Dados", 3, 45, ["--prereq", "Fundamentos de Programação"]),
    (1003, "Mecânica dos Fluidos", 4, 80, []),
    (1004, "Genética", 3, 40, []),
    (1005, "História do Brasil", 2, 30, ["--semestre", "1"]),
    (1006, "Mecânica Clássica", 3, 50, ["--prereq", "Física"]),
]

TURMAS = [
    ("Fundamentos de Programação", "2024.1", 30, "30/09/2024", "SEG 18:00-20:00", "Sala 101"),
    ("Matemática", "2024.1", 30, "30/09/2024", "SEG 18:00-20:00", "Sala 109"),
    ("Estrutura de Dados", "2024.1", 25, "30/09/2024", "TER 18:00-20:00", "Sala 102"),
    ("Mecânica dos Fluidos", "2024.2", 20, "15/10/2024", "QUA 18:00-20:00", "Laboratório de Engenharia"),
    ("Genética", "2024.1", 22, "30/09/2024", "SEG 18:00-20:00", "Auditório Principal"),
    ("História do Brasil", "2024.1", 18, "10/10/2024", "QUA 18:00-20:00", "Sala 205"),
    ("Mecânica Clássica", "2024.1", 24, "15/10/2024", "SEG 20:00-22:00", "Sala 110"),
]

ALUNOS = [
    ("Alice Silva", "alice@example.com", 1001),
    ("Bruno Oliveira", "bruno@example.com", 1002),
    ("Carla Souza", "carla@example.com", 1003),
    ("Diego Fernandes", "diego@example.com", 1004),
    ("Eduarda Costa", "eduarda@example.com", 1005),
    ("Felipe Lima", "felipe@example.com", 1006),
]

# (nome do aluno, id da turma)
MATRICULAS = [
    ("Bruno Oliveira", 2),
    ("Carla Souza", 2),
    ("Diego Fernandes", 4),
    ("Eduarda Costa", 5),
]


# ---------------------------------------------------------------------------
# Estado compartilhado: nome do aluno -> código de matrícula
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def matriculas_alunos():
    return {}


# ---------------------------------------------------------------------------
# Testes (a ordem importa)
# ---------------------------------------------------------------------------

class TestPopularDatabase:

    @pytest.mark.parametrize("curso_id, nome, carga_horaria", CURSOS)
    def test_add_curso(self, curso_id, nome,carga_horaria):
        assert_ok(run_cli("acad", "add_curso", curso_id, nome, carga_horaria))

    @pytest.mark.parametrize("curso_id, nome, creditos, carga, extras", DISCIPLINAS)
    def test_add_disciplina(self, curso_id, nome, creditos, carga, extras):
        assert_ok(run_cli("acad", "add_disciplina", curso_id, nome, creditos, carga, *extras))

    @pytest.mark.parametrize("disciplina, periodo, vagas, data, horario, local", TURMAS)
    def test_add_turma(self, disciplina, periodo, vagas, data, horario, local):
        assert_ok(
            run_cli(
                "acad", "add_turma", disciplina, periodo, vagas, data,
                "--horario", horario,
                "--local", local,
            )
        )

    @pytest.mark.parametrize("nome, email, curso_id", ALUNOS)
    def test_add_aluno(self, nome, email, curso_id, matriculas_alunos):
        result = run_cli("acad", "add_aluno", nome, email, curso_id)
        assert_ok(result)
        matriculas_alunos[nome] = extrair_matricula(result.stdout)

    @pytest.mark.parametrize("nome, turma_id", MATRICULAS)
    def test_matricular(self, nome, turma_id, matriculas_alunos):
        assert nome in matriculas_alunos, (
            f"Matrícula de '{nome}' não foi capturada (test_add_aluno falhou?)"
        )
        codigo = matriculas_alunos[nome]
        assert_ok(run_cli("acad", "matricular", codigo, turma_id))