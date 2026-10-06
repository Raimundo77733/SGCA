import random
from database_methods import Data_link_sql

class Aluno:
    """Aluno armazena listas de matrículas ativas, concluídas e histórico"""

    def __init__(self, nome, email, cod_curso):
        self._n_matricula = 0
        self.nome=nome
        self.email=email
        self.cod_curso = cod_curso
        self._status_curso= 'Cursando'
        self.historico=[]
        self.matriculas_ativas = []
        self.cr=0
        self._database_link=Data_link_sql()

    def __str__(self) :
        return f"Aluno:{self.nome}\nE-mail:{self.email}\nCódigo do Curso:{self.cod_curso}\nCR:{self.cr}\nStatus do curso:{self.status_curso}"

    def __len__(self):
        return 1

    @property
    def status_curso(self):
        return self._status_curso
    @status_curso.setter
    def status_curso(self, status_curso):
        estados_permitidos_matricula = ["Cursando", "Trancada"]
        if self._status_curso in estados_permitidos_matricula:
            self._status_curso = status_curso
        else:
            print("Estado não permitido")

    @property
    def matricula(self):
        return self._n_matricula
    @matricula.setter
    def matricula(self, n_matricula):

        self._n_matricula=n_matricula

    def gerar_n_matricula(self):
            ids = self._database_link.get_numeros_repetidos_matricula()

            while True:
                numero = random.randint(100000, 999999)
                if numero not in ids: break

            return numero
    def calcular_cr(self):
        """Calcula o Coeficiente de Rendimento do aluno"""
        lista_disciplinas=self._database_link.get_historico_database(self.matricula)
        cr=0
        soma_creditos=0
        if lista_disciplinas:
            for disciplina in lista_disciplinas:
                    nota=disciplina[4]
                    creditos=disciplina[5]
                    cr=cr+(nota*creditos)
                    soma_creditos=soma_creditos+creditos
            cr=cr / soma_creditos
            self.cr=cr
            self._database_link.update_aluno_database(self)
            return cr
        return 0

    def mostrar_historico(self):
        """Mostra o histórico acadêmico do aluno"""
        lista_disciplinas=self._database_link.get_historico_database(self.matricula)
        for disciplina in lista_disciplinas:
            print(disciplina)

    def trancar_curso(self):
        """Tranca o curso do aluno"""
        self.status_curso= "Trancado"
        self._database_link.update_aluno_database(self)

    def trancar_disciplina(self,matricula):
        """Tranca uma disciplina específica"""
        matricula.status="Trancada"



