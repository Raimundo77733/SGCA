from src.sgca.domain.Pessoa import Pessoa
from src.sgca.errors.UnauthorizedError import CourseStatusError


class Aluno(Pessoa):
    """Aluno armazena listas de matrículas ativas, concluídas e histórico"""

    def __init__(self, nome, email, cod_curso, nome_curso):
        super().__init__(nome, email)
        self._n_matricula = 0
        self.cod_curso=cod_curso
        self.nome_curso=nome_curso
        self._status_curso = 'Cursando'
        self._cr=0.0

    def __str__(self) :
        return f"Aluno:{self.nome}\nE-mail:{self.email}\nCódigo do Curso:{self.cod_curso}\nCurso:{self.nome_curso}\nCR:{self.cr}\nStatus do curso:{self.status_curso}"

    def __len__(self):
        return 1

    @property
    def status_curso(self):
        return self._status_curso

    @status_curso.setter
    def status_curso(self, status_curso):
        estados_permitidos_curso = ["Cursando", "Trancado"]
        if status_curso not in estados_permitidos_curso:
            raise CourseStatusError(f"Status de curso inválido: {status_curso}")
        self._status_curso = status_curso


    @property
    def matricula(self):
        return self._n_matricula

    @matricula.setter
    def matricula(self, n_matricula):
        self._n_matricula=n_matricula

    @property
    def cr(self):
        return self._cr
    @cr.setter
    def cr(self,cr):
        self._cr=cr
