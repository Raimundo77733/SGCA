import re
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
CLI = SRC / "cli.py"


def run_cli(*args, db=None):
    """Executa o CLI com cwd=src, assim o default 'data/sgca.db'
    resolve para raiz/src/data/sgca.db (e não raiz/data/sgca.db)."""
    (SRC / "data").mkdir(exist_ok=True)
    cmd = [sys.executable, str(CLI)]
    if db is not None:
        cmd += ["--db", str(db)]
    cmd += [str(a) for a in args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)


def assert_ok(result):
    assert result.returncode == 0, (
        f"Falhou com código {result.returncode}\n"
        f"STDOUT: {result.stdout}\n"
        f"STDERR: {result.stderr}"
    )


def assert_negada(result):
    """O CLI imprime 'Erro: ...' e retorna 1 em DatabaseErrors/UnauthorizedError/ValidationError."""
    assert result.returncode == 1, (
        f"Esperava operação negada (código 1), veio {result.returncode}\n"
        f"STDOUT: {result.stdout}\n"
        f"STDERR: {result.stderr}"
    )
    assert "Erro" in result.stdout, f"Sem mensagem de erro no stdout:\n{result.stdout}"


def extrair_matricula(stdout: str) -> str:
    # O CLI imprime: "Criando Alice Silva (454334)"
    match = re.search(r"\((\d+)\)", stdout)
    if match:
        return match.group(1)
    numeros = re.findall(r"\d+", stdout)
    assert numeros, f"Matrícula não encontrada no stdout:\n{stdout}"
    return numeros[-1]