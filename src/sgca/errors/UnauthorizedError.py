class UnauthorizedError(Exception):
    """Quando o usuário não tem permissão para efetuar uma ação"""

class CourseStatusError(UnauthorizedError):
    """O estado atribuido ao curso não é permitido"""

class EstadoMatriculaError(UnauthorizedError):
    """O estado de matrícula atribuído não é aceito"""

class PrazoTrancamentoError(UnauthorizedError):
    """O prazo para trancamento já terminou"""
