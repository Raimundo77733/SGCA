import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'db' / 'mydatabase.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

def criar_tabelas():
        """Cria todas as tabelas do sistema"""

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Curso (
                cod_curso TEXT PRIMARY KEY,
                nome_curso TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Aluno (
                n_matricula TEXT PRIMARY KEY ,
                nome TEXT NOT NULL,
                email TEXT,
                cod_curso TEXT NOT NULL,
                cr INTEGER,
                FOREIGN KEY (cod_curso) REFERENCES Curso(cod_curso)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Turma (
                id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
                cod_curso TEXT NOT NULL,
                nome_disciplina TEXT NOT NULL,
                semestre TEXT,
                vagas_max INTEGER,
                status TEXT DEFAULT 'Aberta',
                carga_horaria INTEGER,
                data_limite TEXT,
                horarios TEXT,
                local TEXT,
                inscritos INTEGER,
                FOREIGN KEY (cod_curso) REFERENCES Curso(cod_curso)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Matricula (
                id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
                n_matricula TEXT NOT NULL,
                id_turma INTEGER NOT NULL,
                data_matricula DATE,
                status TEXT DEFAULT 'Cursando',
                media REAL DEFAULT 0,
                frequencia REAL DEFAULT 0,
                FOREIGN KEY (n_matricula) REFERENCES Aluno(n_matricula),
                FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
                UNIQUE(n_matricula, id_turma)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Historico (
                id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
                n_matricula TEXT NOT NULL,
                nome_disciplina TEXT NOT NULL,
                semestre TEXT,
                nota_final REAL,
                status TEXT,
                data_conclusao DATE,
                FOREIGN KEY (n_matricula) REFERENCES Aluno(n_matricula)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                semestre INTEGER,
                cod_curso INTEGER NOT NULL,
                prerequisitos TEXT NOT NULL,
                FOREIGN KEY (cod_curso) REFERENCES Curso (cod_curso)
            )
        ''')

        connection.commit()
criar_tabelas()