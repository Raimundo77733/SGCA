from errors.Validation import CodigoCursoInvalidoErro


class Curso:
    """Curso armazena o nome do curso e o código do curso e a carga horária a disciplinas são adicionadas posteriormente"""

    def __init__(self,nome_curso,cod_curso,carga_horaria):
        self.nome_curso = nome_curso
        self.cod_curso = cod_curso
        self.carga_horaria=carga_horaria
        self.disciplinas=""


    @property
    def cod_curso(self):
        return self._cod_curso

    @cod_curso.setter
    def cod_curso(self,cod_curso):
        try:
            numero = int(cod_curso)
        except (TypeError, ValueError):
            raise CodigoCursoInvalidoErro("O código do curso deve ser um número.")
        if not 1000 <= numero <= 9999:
            raise CodigoCursoInvalidoErro("O código do curso deve estar entre 1000 e 9999.")
        self._cod_curso = str(numero)
