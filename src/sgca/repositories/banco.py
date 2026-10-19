"""Único ponto de contato com o SQLite.

Ninguém fora deste arquivo importa `sqlite3`. A conexão é criada uma vez
(no bootstrap) e entregue aos repositórios.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from src.sgca.errors.DatabaseErrors import IntegridadeError, JaExisteError, CommitError


def _determinar_tipo_erro(erro):
    texto = str(erro)
    if "UNIQUE" in texto or "PRIMARY KEY" in texto:
        #Caso haja tentativa de gravar dados sobre uma chave única
        return JaExisteError("Já existe um registro com esses dados.")
    if "FOREIGN KEY" in texto:
        #Caso as chaves sejam inválidas ou haja problemas de alinhamento entre o banco e os objetos
        return IntegridadeError(
            "Operação inválida: o registro referencia algo inexistente "
            "ou ainda é referenciado por outros registros.")
    return IntegridadeError(f"Violação de integridade: {texto}")
    #Caso genérico em que o tipo de erro viola a integridade, mas não tem relação com a chave única ou estrangeira


class Banco:
    def __init__(self, caminho=":memory:"):
        #Caminho definido para memória se não especificado, na CLI o endereço da db pode ser inserido
        if str(caminho) != ":memory:":
            Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        self._database_link = sqlite3.connect(caminho)
        self._database_link.row_factory = sqlite3.Row
        #Equivalente a mudar a configuração de como as linhas são exibidas substitui o atributo row_factory
        #pela classe sqlite3.Row que processa a linha e retorna um objeto sqlite3.Row que pode ser acessado
        #por linha[0] ou linha["nome"]
        self._database_link.execute("PRAGMA foreign_keys = ON")
        #PRAGMA FOREING KEY 1, significa que as tabelas ligadas com JOIN,
        #não podem criar conexões entre colunas com chaves inexistentes ou excluir com dependências de outras tabelas
        self._nivel = 0
        #nível da transação

    def executar(self, sql, params=()):
        try:
            return self._database_link.execute(sql, params)
        except sqlite3.IntegrityError as erro:
            raise _determinar_tipo_erro(erro) from erro

    def fetch_one_line(self, sql, params=()):
        #quando for necessário retornar uma linha
        cursor = self.executar(sql, params)
        linha = cursor.fetchone()
        return linha

    def fetch_all_lines(self, sql, params=()):
        #quando for necessário retornar várias linhas
        cursor = self.executar(sql, params)
        linhas = cursor.fetchall()
        return linhas

    @contextmanager
    def transacao(self):
        """Agrupa gravações para facilitar o rollback,
        utilizada para efetuar transações na database e evitar erros por transações incompletas
        """
        self._nivel += 1
        #nível aumenta em 1 toda vez que a transação de database é chamada
        try:
            yield
            #A transação pula para o with que será usado no atulizar, inserir e remover
        except BaseException:
            #Erro na transação
            self._nivel -= 1
            #nível volta ao banco
            if self._nivel == 0:
                #rollback
                self._database_link.rollback()
            raise
            #Redireciona o erro do except para o executar que determina os tipos listados
            #Caminho da falha Try->yield-> with->executar->transacao->except->raise->
            #                   _determinar_tipo_erro(erro)-> determinado tipo já existe| tipo integridade erro
            #                   |tipo integridade indeterminada
        else:
            self._nivel -= 1
            if self._nivel == 0:
                self._database_link.commit()
                #Caminho do sucesso de transação Try->yield-> with-> executar->transacao->retoma do yield->else->commit


    def fechar(self):
        self._database_link.close()
