"""
Regras de negócio. Cada teste usa um banco novo e isolado (tmp_path, via --db),
então não depende do test_1_populate nem suja o banco de src/data.

Suposições (ajuste as constantes/asserts se o seu sistema for diferente):
  - IDs de turma são autoincrementais a partir de 1 em banco vazio.
  - Média da turma = média aritmética das avaliações lançadas.
  - CR = média das notas finais ponderada pelos créditos.
"""
import re

import pytest

from helpers import assert_negada, assert_ok, extrair_matricula, run_cli

SEMESTRE = "2030.1"
DATA_LIMITE = "30/09/2030"
DATA_AULA = "15/10/2030"
NOTA_MIN = 5.0
FREQ_MIN = 75


class SGCA:
    def __init__(self, db):
        self.db = db
        self._turmas = 0

    def run(self, *args):
        return run_cli(*args, db=self.db)

    def ok(self, *args):
        r = self.run(*args)
        assert_ok(r)
        return r

    # --- montagem de cenário ---
    def curso(self, cod=1001, nome="Ciência da Computação"):
        self.ok("acad", "add_curso", cod, nome, 3600)

    def disciplina(self, nome, creditos=4, cod_curso=1001, prereq=()):
        extras = []
        for p in prereq:
            extras += ["--prereq", p]
        self.ok("acad", "add_disciplina", cod_curso, nome, creditos, 60, *extras)

    def turma(self, disciplina, horario="SEG 18:00-20:00", vagas=30):
        self.ok("acad", "add_turma", disciplina, SEMESTRE, vagas, DATA_LIMITE,
                "--horario", horario, "--local", "Sala 1")
        self._turmas += 1
        return self._turmas

    def aluno(self, nome, cod_curso=1001):
        email = nome.split()[0].lower() + "@example.com"
        r = self.ok("acad", "add_aluno", nome, email, cod_curso)
        return extrair_matricula(r.stdout)

    # --- ações ---
    def matricular(self, mat, turma):
        return self.ok("acad", "matricular", mat, turma)

    def lancar(self, mat, turma, nota, avaliacao="AB1"):
        return self.ok("acad", "lancar_nota", mat, turma, avaliacao, nota)

    def presenca(self, mat, turma):
        return self.ok("acad", "lancar_frequencia", mat, turma, DATA_AULA, "presente")

    def concluir(self, turma):
        return self.ok("acad", "concluir_disciplina", turma,
                       "--nota_minima", NOTA_MIN, "--frequencia_minima", FREQ_MIN)

    def cursar(self, mat, turma, nota):
        """matricula + nota + presença (não conclui a turma)."""
        self.matricular(mat, turma)
        self.lancar(mat, turma, nota)
        self.presenca(mat, turma)


@pytest.fixture
def sgca(tmp_path):
    s = SGCA(tmp_path / "sgca_test.db")
    s.curso()
    return s


def ordem_correta(stdout, nomes):
    pos = [stdout.find(n) for n in nomes]
    assert all(p >= 0 for p in pos), f"Nem todos os nomes apareceram:\n{stdout}"
    assert pos == sorted(pos), f"Ordem esperada {nomes}, saída:\n{stdout}"


# ---------------------------------------------------------------------------
# Matrícula negada
# ---------------------------------------------------------------------------

class TestPrerequisito:
    def test_sem_prerequisito_negada(self, sgca):
        sgca.disciplina("Matemática")
        sgca.disciplina("Fundamentos de Programação", prereq=["Matemática"])
        sgca.turma("Matemática")
        t_fp = sgca.turma("Fundamentos de Programação", horario="TER 18:00-20:00")
        mat = sgca.aluno("Alice Silva")

        assert_negada(sgca.run("acad", "matricular", mat, t_fp))

    def test_com_prerequisito_cumprido_permitida(self, sgca):
        sgca.disciplina("Matemática")
        sgca.disciplina("Fundamentos de Programação", prereq=["Matemática"])
        t_mat = sgca.turma("Matemática")
        t_fp = sgca.turma("Fundamentos de Programação", horario="TER 18:00-20:00")
        mat = sgca.aluno("Alice Silva")

        sgca.cursar(mat, t_mat, 8.0)
        sgca.concluir(t_mat)

        assert_ok(sgca.run("acad", "matricular", mat, t_fp))


class TestChoqueHorario:
    @pytest.mark.parametrize("horario_b, permitida", [
        ("SEG 18:00-20:00", False),   # idêntico
        ("SEG 19:00-21:00", False),   # sobreposição parcial
        ("SEG 20:00-22:00", True),    # colado, sem sobreposição
        ("QUA 18:00-20:00", True),    # outro dia
    ])
    def test_choque(self, sgca, horario_b, permitida):
        sgca.disciplina("Matemática")
        sgca.disciplina("Física")
        t_a = sgca.turma("Matemática", horario="SEG 18:00-20:00")
        t_b = sgca.turma("Física", horario=horario_b)
        mat = sgca.aluno("Alice Silva")

        sgca.matricular(mat, t_a)
        r = sgca.run("acad", "matricular", mat, t_b)
        if permitida:
            assert_ok(r)
        else:
            assert_negada(r)


class TestTurmaLotada:
    def test_turma_lotada_negada(self, sgca):
        sgca.disciplina("Matemática")
        t = sgca.turma("Matemática", vagas=1)
        alice = sgca.aluno("Alice Silva")
        bruno = sgca.aluno("Bruno Oliveira")

        sgca.matricular(alice, t)
        assert_negada(sgca.run("acad", "matricular", bruno, t))

    def test_ultima_vaga_permitida(self, sgca):
        sgca.disciplina("Matemática")
        t = sgca.turma("Matemática", vagas=2)
        sgca.matricular(sgca.aluno("Alice Silva"), t)
        assert_ok(sgca.run("acad", "matricular", sgca.aluno("Bruno Oliveira"), t))


# ---------------------------------------------------------------------------
# Notas
# ---------------------------------------------------------------------------

class TestNotas:
    @pytest.fixture
    def cenario(self, sgca):
        sgca.disciplina("Matemática")
        t = sgca.turma("Matemática")
        mat = sgca.aluno("Alice Silva")
        sgca.matricular(mat, t)
        return sgca, mat, t

    def test_lancar_nota_retorna_media(self, cenario):
        sgca, mat, t = cenario
        r = sgca.lancar(mat, t, 8.0, "AB1")
        assert "Média atual: 8.00" in r.stdout

    def test_media_com_duas_avaliacoes(self, cenario):
        sgca, mat, t = cenario
        sgca.lancar(mat, t, 8.0, "AB1")
        r = sgca.lancar(mat, t, 6.0, "AB2")
        assert "Média atual: 7.00" in r.stdout

    @pytest.mark.parametrize("nota", [-0.5, 10.5])
    def test_nota_fora_do_intervalo_negada(self, cenario, nota):
        sgca, mat, t = cenario
        assert_negada(sgca.run("acad", "lancar_nota", mat, t, "AB1", nota))

    @pytest.mark.parametrize("nota", [0, 10])
    def test_nota_nos_limites_aceita(self, cenario, nota):
        sgca, mat, t = cenario
        assert_ok(sgca.run("acad", "lancar_nota", mat, t, "AB1", nota))

    def test_nota_para_aluno_nao_matriculado_negada(self, cenario):
        sgca, _, t = cenario
        outro = sgca.aluno("Bruno Oliveira")
        assert_negada(sgca.run("acad", "lancar_nota", outro, t, "AB1", 7.0))


# ---------------------------------------------------------------------------
# CR e Top N
# ---------------------------------------------------------------------------

class TestCRTopN:
    @pytest.fixture
    def cenario(self, sgca):
        """D1 (4 créditos) e D2 (2 créditos).
        Alice: 9 e 6 -> CR ponderado 8.0 (aritmético 7.5)
        Bruno: 7 e 7 -> 7.0
        Carla: 5 e 5 -> 5.0"""
        sgca.disciplina("Cálculo", creditos=4)
        sgca.disciplina("Lógica", creditos=2)
        t1 = sgca.turma("Cálculo", horario="SEG 18:00-20:00")
        t2 = sgca.turma("Lógica", horario="TER 18:00-20:00")
        alunos = {n: sgca.aluno(n) for n in ("Alice Silva", "Bruno Oliveira", "Carla Souza")}
        notas = {
            "Alice Silva": (9.0, 6.0),
            "Bruno Oliveira": (7.0, 7.0),
            "Carla Souza": (5.0, 5.0),
        }
        for nome, mat in alunos.items():
            sgca.cursar(mat, t1, notas[nome][0])
            sgca.cursar(mat, t2, notas[nome][1])
        return sgca, alunos, t1, t2

    def test_top_turma_parcial_ordenado(self, cenario):
        sgca, _, t1, _ = cenario
        r = sgca.ok("acad", "top_nt", t1)
        ordem_correta(r.stdout, ["Alice Silva", "Bruno Oliveira", "Carla Souza"])
        assert "temporária" in r.stdout  # turma ainda cursando

    def test_top_turma_concluida_ordenado(self, cenario):
        sgca, _, t1, _ = cenario
        sgca.concluir(t1)
        r = sgca.ok("acad", "top_nt", t1)
        ordem_correta(r.stdout, ["Alice Silva", "Bruno Oliveira", "Carla Souza"])
        assert "temporária" not in r.stdout
        assert re.search(r"9[.,]0", r.stdout)

    def test_top_curso_ordenado_e_cr_ponderado(self, cenario):
        sgca, _, t1, t2 = cenario
        sgca.concluir(t1)
        sgca.concluir(t2)
        r = sgca.ok("acad", "top_nc", 1001)
        ordem_correta(r.stdout, ["Alice Silva", "Bruno Oliveira", "Carla Souza"])

        # CR = média das notas finais ponderada pelos créditos
        # Alice: (9*4 + 6*2) / 6 = 8.0  (média simples daria 7.5)
        esperado = {"Alice Silva": 8.0, "Bruno Oliveira": 7.0, "Carla Souza": 5.0}
        for nome, cr in esperado.items():
            m = re.search(rf"Aluno:{nome}.*?CR:\s*([\d.,]+)", r.stdout, re.DOTALL)
            assert m, f"CR de {nome} não encontrado:\n{r.stdout}"
            assert float(m.group(1).replace(",", ".")) == pytest.approx(cr, abs=0.01), (
                f"CR de {nome}: esperado {cr}, veio {m.group(1)}"
            )

    def test_historico_apos_conclusao(self, cenario):
        sgca, alunos, t1, t2 = cenario
        sgca.concluir(t1)
        sgca.concluir(t2)
        r = sgca.ok("acad", "hist_aluno", alunos["Alice Silva"])
        assert "Cálculo" in r.stdout and "Lógica" in r.stdout
        assert "APROVADO" in r.stdout


# ---------------------------------------------------------------------------
# Trancamento
# ---------------------------------------------------------------------------

class TestTrancamentoDisciplina:
    @pytest.fixture
    def cenario(self, sgca):
        sgca.disciplina("Matemática")
        t = sgca.turma("Matemática", vagas=10)
        mat = sgca.aluno("Alice Silva")
        sgca.matricular(mat, t)
        return sgca, mat, t

    def test_trancar_libera_vaga(self, cenario):
        sgca, mat, t = cenario
        assert "Vagas:1/" in sgca.ok("acad", "list_alunos_turma", t).stdout

        r = sgca.run("acad", "trancar_disciplina", mat, t)
        assert_ok(r)
        assert f"trancada na turma {t}" in r.stdout
        assert "Vagas:0/" in sgca.ok("acad", "list_alunos_turma", t).stdout

    def test_trancar_registra_historico_como_trancada(self, cenario):
        sgca, mat, t = cenario
        sgca.ok("acad", "trancar_disciplina", mat, t)

        # sai da turma...
        assert mat not in sgca.ok("acad", "list_alunos_turma", t).stdout
        # ...mas fica no histórico com status Trancada
        hist = sgca.ok("acad", "hist_aluno", mat).stdout
        assert "Matemática" in hist
        assert "Trancada" in hist

    def test_nota_apos_trancamento_negada(self, cenario):
        sgca, mat, t = cenario
        sgca.ok("acad", "trancar_disciplina", mat, t)
        assert_negada(sgca.run("acad", "lancar_nota", mat, t, "AB1", 7.0))

    def test_trancar_sem_matricula_negada(self, sgca):
        sgca.disciplina("Matemática")
        t = sgca.turma("Matemática")
        mat = sgca.aluno("Alice Silva")
        assert_negada(sgca.run("acad", "trancar_disciplina", mat, t))


class TestTrancamentoCurso:
    @pytest.fixture
    def cenario(self, sgca):
        sgca.disciplina("Matemática")
        sgca.disciplina("Física")
        sgca.disciplina("Biologia")
        t1 = sgca.turma("Matemática", horario="SEG 18:00-20:00")
        t2 = sgca.turma("Física", horario="TER 18:00-20:00")
        t3 = sgca.turma("Biologia", horario="QUA 18:00-20:00")
        mat = sgca.aluno("Alice Silva")
        sgca.matricular(mat, t1)
        sgca.matricular(mat, t2)
        return sgca, mat, t1, t2, t3

    def test_trancar_curso_remove_de_todas_as_turmas_e_registra_historico(self, cenario):
        sgca, mat, t1, t2, _ = cenario
        r = sgca.run("acad", "trancar_curso", mat)
        assert_ok(r)
        assert "trancado" in r.stdout

        for t in (t1, t2):
            out = sgca.ok("acad", "list_alunos_turma", t).stdout
            assert "Vagas:0/" in out
            assert mat not in out

        hist = sgca.ok("acad", "hist_aluno", mat).stdout
        assert "Matemática" in hist and "Física" in hist
        assert hist.count("Trancada") == 2

    def test_trancar_curso_so_tranca_matriculas_cursando(self, cenario):
        sgca, mat, t1, t2, t3 = cenario
        # conclui Biologia (t3) antes de trancar o curso
        sgca.cursar(mat, t3, 8.0)
        sgca.concluir(t3)

        sgca.ok("acad", "trancar_curso", mat)

        hist = sgca.ok("acad", "hist_aluno", mat).stdout
        linhas = {l.split(" - ")[0]: l for l in hist.splitlines() if l.strip()}
        assert "Trancada" in linhas["Nome da Disciplina:Matemática"]
        assert "Trancada" in linhas["Nome da Disciplina:Física"]
        assert "APROVADO" in linhas["Nome da Disciplina:Biologia"]
        assert "Trancada" not in linhas["Nome da Disciplina:Biologia"]

    def test_trancar_curso_muda_status_do_aluno(self, cenario):
        sgca, mat, *_ = cenario
        antes = sgca.ok("acad", "busc_aluno", mat).stdout
        assert "Status do curso:Trancado" not in antes

        sgca.ok("acad", "trancar_curso", mat)
        depois = sgca.ok("acad", "busc_aluno", mat).stdout
        assert "Status do curso:Trancado" in depois

    def test_matricular_apos_trancar_curso_negada(self, cenario):
        sgca, mat, _, _, t3 = cenario
        sgca.ok("acad", "trancar_curso", mat)
        assert_negada(sgca.run("acad", "matricular", mat, t3))

    def test_trancar_curso_nao_afeta_outros_alunos(self, cenario):
        sgca, mat, t1, _, _ = cenario
        outro = sgca.aluno("Bruno Oliveira")
        sgca.matricular(outro, t1)
        sgca.ok("acad", "trancar_curso", mat)
        assert "Vagas:1/" in sgca.ok("acad", "list_alunos_turma", t1).stdout