def criar_tabelas(banco):
    with banco.transacao():
        banco.executar("""
            CREATE TABLE IF NOT EXISTS Curso (
                cod_curso TEXT PRIMARY KEY,
                nome_curso TEXT NOT NULL
            )""")
        banco.executar("""
            CREATE TABLE IF NOT EXISTS Aluno (
                n_matricula TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT,
                cod_curso TEXT NOT NULL,
                nome_curso TEXT NOT NULL,
                cr REAL DEFAULT 0,
                status_curso TEXT NOT NULL DEFAULT 'Cursando',
                FOREIGN KEY (cod_curso) REFERENCES Curso(cod_curso)
            )""")
        banco.executar("""
            CREATE TABLE IF NOT EXISTS Turma (
                id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
                id_disciplina INTEGER NOT NULL,
                semestre TEXT,
                vagas_max INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aberta',
                data_limite TEXT,
                horarios TEXT,
                local TEXT,
                inscritos INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (id_disciplina) REFERENCES Disciplinas(id)
            )""")
        banco.executar("""
            CREATE TABLE IF NOT EXISTS Matricula (
                id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
                n_matricula TEXT NOT NULL,
                id_turma INTEGER NOT NULL,
                data_matricula TEXT,
                status TEXT NOT NULL DEFAULT 'Cursando',
                media REAL DEFAULT 0,
                frequencia_media REAL DEFAULT 0,
                notas TEXT DEFAULT '{}',
                registro_frequencia TEXT DEFAULT '{}',
                FOREIGN KEY (n_matricula) REFERENCES Aluno(n_matricula),
                FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
                UNIQUE(n_matricula, id_turma)
            )""")
        banco.executar("""
            CREATE TABLE IF NOT EXISTS Historico (
                id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
                n_matricula TEXT NOT NULL,
                nome_disciplina TEXT NOT NULL,
                semestre TEXT,
                nota_final REAL,
                status TEXT,
                creditos REAL NOT NULL DEFAULT 0,
                data_conclusao TEXT,
                FOREIGN KEY (n_matricula) REFERENCES Aluno(n_matricula)
            )""")
        banco.executar("""
            CREATE TABLE IF NOT EXISTS Disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                semestre INTEGER,
                cod_curso TEXT NOT NULL,
                creditos REAL NOT NULL DEFAULT 0,
                carga_horaria INTEGER,
                prerequisitos TEXT NOT NULL DEFAULT '',
                FOREIGN KEY (cod_curso) REFERENCES Curso(cod_curso)
            )""")
