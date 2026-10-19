
from  src.sgca.errors.DatabaseErrors import NaoEncontradoError

class Repositorio:
    """Classe genérica CRUD"""
    TABELA = ""
    CHAVE = ()                 # colunas da chave (uma ou mais)
    AUTO_INCREMENT = False     # chave gerada pelo banco?
    SELECT = None              # SELECT base (padrão: SELECT * FROM TABELA)
    CHAVE_SELECT = None        # chave qualificada, se SELECT usar alias

    def __init__(self, banco):
        self.banco = banco

    #Funções de conversão de objeto para dicionário, são subscritas pelos repos específicos
    def _para_linha(self, obj):
        raise NotImplementedError

    def _para_objeto(self, linha):
        raise NotImplementedError

    def _definir_chave(self, obj, valor):
        raise NotImplementedError

    def _select(self):
        #Default select subscrito pelo repo se houver 
        if self.SELECT:
            return self.SELECT
        return f"SELECT * FROM {self.TABELA}"

    def _where(self, colunas):
        #retorna a coluna com ? para a segurança
        #ex nome numero = nome=? AND numero=?
        condicoes = []
        for coluna in colunas:
            condicoes.append(f"{coluna} = ?")
        return " AND ".join(condicoes)

    @staticmethod
    def _rotulo(chave):
        partes = []
        for parte in chave:
            partes.append(str(parte))
        return ", ".join(partes)

    def _checar(self, chave):
        if len(chave) != len(self.CHAVE):
            raise TypeError(f"{self.TABELA} espera a chave {self.CHAVE}, recebeu {chave}")

    def _consultar(self, complemento="", params=()):
        linhas = self.banco.fetch_all_lines(f"{self._select()} {complemento}", params)
        objetos = []
        for linha in linhas:
            objetos.append(self._para_objeto(linha))
        return objetos
    
    #Busca e obter estão mesclados, possível problema que precisa de simplificação
    def buscar(self, *chave):
        """Devolve o objeto ou None."""
        self._checar(chave)
        where = self._where(self.CHAVE_SELECT or self.CHAVE)
        linha = self.banco.fetch_one_line(f"{self._select()} WHERE {where}", chave)
        if linha is None:
            return None
        objeto = self._para_objeto(linha)
        return objeto

    def obter(self, *chave):
        """Devolve o objeto ou levanta NaoEncontradoError."""
        objeto = self.buscar(*chave)
        if objeto is None:
            raise NaoEncontradoError(f"{self.TABELA} {self._rotulo(chave)} não encontrado(a).")
        return objeto

    def existe(self, *chave):
        self._checar(chave)
        sql = f"SELECT 1 FROM {self.TABELA} WHERE {self._where(self.CHAVE)}"
        linha = self.banco.fetch_one_line(sql, chave)
        if linha is None:
            return False
        return True

    def listar(self):
        ordem = ", ".join(self.CHAVE_SELECT or self.CHAVE)
        return self._consultar(f"ORDER BY {ordem}")

    def inserir(self, obj):

        dados = self._para_linha(obj)
        if self.AUTO_INCREMENT:
            for coluna in self.CHAVE:
                dados.pop(coluna, None)
        colunas = ", ".join(dados)
        marcas = ", ".join("?" for _ in dados)
        with self.banco.transacao():
            cursor = self.banco.executar(
                f"INSERT INTO {self.TABELA} ({colunas}) VALUES ({marcas})",
                tuple(dados.values()))
        if self.AUTO_INCREMENT:
            self._definir_chave(obj, cursor.lastrowid)
        return obj

    def atualizar(self, obj):
        """Atualiza pela chave. A chave em si não pode ser alterada."""
        dados = self._para_linha(obj)
        chave = tuple(dados.pop(c) for c in self.CHAVE)
        sets = ", ".join(f"{c} = ?" for c in dados)
        with self.banco.transacao():
            cursor = self.banco.executar(
                f"UPDATE {self.TABELA} SET {sets} WHERE {self._where(self.CHAVE)}",
                (*dados.values(), *chave))
            if cursor.rowcount == 0:
                raise NaoEncontradoError(f"{self.TABELA} {self._rotulo(chave)} não encontrado(a).")
        return obj

    def remover(self, *chave):
        self._checar(chave)
        with self.banco.transacao():
            cursor = self.banco.executar(
                f"DELETE FROM {self.TABELA} WHERE {self._where(self.CHAVE)}", chave)
            if cursor.rowcount == 0:
                raise NaoEncontradoError(f"{self.TABELA} {self._rotulo(chave)} não encontrado(a).")
