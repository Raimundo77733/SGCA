from Class.Aluno import Aluno
import pytest

from Class.Secretaria import Secretaria

aluno=Aluno("Pedro","Pedro@gmail.com",22)
administrador=Secretaria("Jorge","Jorge@gmail.com",5555)

def test_aluno_print():
    assert aluno.__str__() == "Aluno:Pedro\nE-mail:Pedro@gmail.com\nCódigo do Curso:22\nCR:0\nStatus do curso:Cursando"
def test_aluno_matricula():
    '''Property'''
    aluno.matricula=22
    assert aluno.matricula==22
    assert administrador.cadastrar_aluno(aluno)=="Tentativa de cadastro com número de matrícula inválido"
def test_aluno_escrita():
    aluno.matricula=555555
    administrador.cadastrar_aluno(aluno)
def test_aluno_recover():
    aluno=administrador.get_aluno_por_matricula(555555)
    assert aluno.__str__() == "Aluno:Pedro\nE-mail:Pedro@gmail.com\nCódigo do Curso:22\nCR:0\nStatus do curso:Cursando"
def test_remove_aluno():
    administrador.remover_aluno(555555)




