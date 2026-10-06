import sqlite3
from pathlib import Path

from database_init import connection


class Data_link_sql:
    def __init__(self):
        '''Database Link'''
        db_path = Path(__file__).parent / 'db' / 'mydatabase.db'
        self.database_link = sqlite3.connect(db_path)
        self.cursor = self.database_link.cursor()

    ''''Secretaria'''

    def novo_aluno_database(self, aluno):
        self.cursor.execute('''INSERT INTO Aluno (n_matricula, nome, email, cod_curso, cr) 
                              VALUES (?, ?, ?, ?, ?)''',
                            (aluno.matricula, aluno.nome, aluno.email, aluno.cod_curso, aluno.cr))
        self.database_link.commit()

    def get_lista_cursos_database(self):
        self.cursor.execute('''SELECT DISTINCT * FROM Curso ''')
        cursos = self.cursor.fetchall()
        return cursos

    def get_aluno_database(self,n_matricula):
        self.cursor.execute('''SELECT * FROM Aluno WHERE n_matricula = ?''', (n_matricula,))
        database_line = self.cursor.fetchone()
        return database_line

    def update_aluno_database(self, aluno):
        self.cursor.execute('''UPDATE Aluno SET 
                              n_matricula = ?, 
                              nome = ?, 
                              email = ?, 
                              cod_curso = ?, 
                              cr = ? 
                              WHERE n_matricula = ?''',
                            (aluno.matricula, aluno.nome, aluno.email, aluno.cod_curso, aluno.cr,
                             aluno.matricula))
        self.database_link.commit()

    def remove_aluno_database(self, numero_matricula):
        self.cursor.execute('''DELETE FROM Aluno WHERE n_matricula = ?''', (numero_matricula,))
        self.database_link.commit()


    def get_numeros_repetidos_matricula(self):
        self.cursor.execute("SELECT n_matricula FROM Aluno")
        ids = [row[0] for row in self.cursor.fetchall()]
        return ids

    '''Curso'''

    def insert_curso_database(self, curso):
        self.cursor.execute('''INSERT INTO Curso (cod_curso, nome_curso) 
                              VALUES (?, ?)''', (curso.cod_curso, curso.nome_curso))
        self.database_link.commit()

    def update_curso_database(self, curso):
        self.cursor.execute('''UPDATE Curso SET 
                              cod_curso = ?, 
                              nome_curso = ? 
                              WHERE cod_curso = ?''',
                            (curso.cod_curso, curso.nome_curso, curso.cod_curso))
        self.database_link.commit()

    def remove_curso_database(self, cod_curso):
        self.cursor.execute('''DELETE FROM Curso WHERE cod_curso = ?''', (cod_curso,))
        self.database_link.commit()

    def lista_alunos_curso_database(self,cod_curso):
        self.cursor.execute('''SELECT * FROM Aluno WHERE cod_curso = ?''', (cod_curso,))
        database_lines = self.cursor.fetchall()
        return database_lines

    def get_disciplinas_do_curso_database(self,cod_curso):
        self.cursor.execute('''SELECT * FROM Disciplinas WHERE cod_curso = ?''', (cod_curso,))
        database_lines = self.cursor.fetchall()
        return database_lines

    def get_topn_database(self,cod_curso):
        temp_value=10
        self.cursor.execute('''SELECT * FROM Aluno WHERE cod_curso = ? ORDER BY cr DESC LIMIT (?)''', (cod_curso,temp_value))
        database_lines = self.cursor.fetchall()
        return database_lines
    def get_risco_database(self,cod_curso):
        temp_value=10
        self.cursor.execute('''SELECT * FROM Aluno WHERE cod_curso = ? ORDER BY cr DESC LIMIT (?)''', (cod_curso,temp_value))
        database_lines = self.cursor.fetchall()
        return database_lines
    '''Aluno'''
    def get_historico_database(self,n_matricula):
        self.cursor.execute('''SELECT * FROM Historico WHERE n_matricula = ? ''',
                            (n_matricula,))
        database_lines = self.cursor.fetchall()
        return database_lines
    '''Matricula'''
    def nova_matricula_database(self, matricula):
        self.cursor.execute('''INSERT INTO Matricula 
                              n_matricula = ?, 
                              id_turma = ?, 
                              cod_curso = ?, 
                              notas = ?, 
                              frequencia_media = ?, 
                              status = ? 
                              WHERE n_matricula = ?''',
                            (matricula.n_matricula, matricula.id_turma, matricula.cod_curso,
                             matricula.notas,
                             matricula.frequencia_media, matricula.status, matricula.n_matricula))
        self.database_link.commit()
    def update_matricula_database(self, matricula):
        self.cursor.execute('''UPDATE Matricula SET 
                              n_matricula = ?, 
                              id_turma = ?, 
                              cod_curso = ?, 
                              notas = ?, 
                              frequencia_media = ?, 
                              status = ? 
                              WHERE n_matricula = ?''',
                            (matricula.n_matricula, matricula.id_turma, matricula.email, matricula.cod_curso,
                             matricula.notas,
                             matricula.frequencia_media, matricula.status, matricula.n_matricula))
        self.database_link.commit()
    '''Turma'''

    def nova_turma_database(self, turma):
        self.cursor.execute('''INSERT INTO Turma (id_turma, cod_curso, nome_disciplina, semestre, vagas_max, status, carga_horaria, data_limite, horarios, local, inscritos) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (turma.id_turma, turma.cod_curso, turma.nome_disciplina, turma.semestre, turma.vagas_max,
                             turma.status,
                             turma.carga_horaria, turma.data_limite, turma.horarios, turma.local, turma.inscritos))
        self.database_link.commit()

    def update_turma_database(self, turma):
        self.cursor.execute('''UPDATE Turma SET 
                              id_turma = ?, 
                              cod_curso = ?, 
                              nome_disciplina = ?, 
                              semestre = ?, 
                              vagas_max = ?, 
                              status = ?, 
                              carga_horaria = ?, 
                              data_limite = ?, 
                              horarios = ?, 
                              local = ?, 
                              inscritos = ? 
                              WHERE id_turma = ?''',
                            (turma.id_turma, turma.cod_curso, turma.nome_disciplina, turma.semestre, turma.vagas_max,
                             turma.status,
                             turma.carga_horaria, turma.data_limite, turma.horarios, turma.local, turma.inscritos,
                             turma.id_turma))
        self.database_link.commit()

    def remove_turma_database(self, id_turma):
        self.cursor.execute('''DELETE FROM Turma WHERE id_turma = ?''', (id_turma,))
        self.database_link.commit()

    def get_lista_alunos_turma(self,id_turma):
        self.cursor.execute('''SELECT a.n_matricula, a.nome, a.email
                                FROM Aluno a
                                INNER JOIN Matricula m ON a.n_matricula = m.n_matricula
                                WHERE m.id_turma = ?''',(id_turma,))
        database_lines=self.cursor.fetchall()
        return database_lines
    def get_turma_database(self,id_turma):
        self.cursor.execute('''SELECT * FROM Turma WHERE id_turma = ?''',(id_turma,))
        turma_data=self.cursor.fetchone()
        return turma_data

    def get_disciplina_database(self,nome_disciplina):
        self.cursor.execute('''SELECT * FROM Disciplinas WHERE nome_disciplina = ?''', (nome_disciplina,))
        database_lines = self.cursor.fetchone()
        return database_lines

    def get_requisitos_disciplina_database(self,nome_disciplina):
        self.cursor.execute('''SELECT prerequisitos FROM Disciplinas WHERE nome_disciplina = ?''', (nome_disciplina,))
        database_lines = self.cursor.fetchone()
        return database_lines

