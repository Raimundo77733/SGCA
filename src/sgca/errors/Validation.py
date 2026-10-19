class ValidationError(Exception):
    """Erros relacionados a validação"""

class MatriculaInvalidaError(ValidationError):
    """Número de matrícula fora da faixa permitida."""

class TurmaFechadaError(ValidationError):
    """Matrícula em turma que não está aberta."""

class TurmaCheiaError(ValidationError):
    """Não há vagas na turma."""

class PreRequisitoError(ValidationError):
    """O aluno não cumpriu os pré-requisitos da disciplina."""

class EstadoInvalidoError(ValidationError):
    """Mudança de estado não permitida (ex.: trancar o que já foi trancado)."""

class CodigoCursoInvalidoErro(ValidationError):
    """O número do código do curso não está no limite entre 1000-9999"""

class HorarioInvalidoError(ValidationError):
    """O horário não está no formato 'SEG 18:00-20:00'."""

class ChoqueHorarioError(ValidationError):
    """A turma tem horário em conflito com outra turma do aluno no mesmo semestre."""

class NotaInvalidaError(ValidationError):
    """A nota está fora do intervalo 0-10."""

class FrequenciaInvalidaError(ValidationError):
    """O registro de frequência é inválido."""
