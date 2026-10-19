class DatabaseErrors(Exception):
    """Erros relacionados com o banco de dados"""
class NaoEncontradoError(DatabaseErrors):
    """A consulta ao banco de dados não retornou dados"""

class JaExisteError(DatabaseErrors):
    """Já existe um registro com a mesma chave."""

class IntegridadeError(DatabaseErrors):
    """A operação quebraria uma relação entre registros (ex.: curso inexistente)."""
class CommitError(DatabaseErrors):
    """A transação com a database não foi completada"""