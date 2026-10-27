python cli.py acad add_curso 1001 "Ciência da Computação"  
python cli.py acad add_curso 1002 "Matemática"  
python cli.py acad add_curso 1003 "Engenharia Civil"  
python cli.py acad add_curso 1004 "Biologia"  
python cli.py acad add_curso 1005 "História"  
python cli.py acad add_curso 1006 "Física"
python cli.py acad add_disciplina 1006 "Física" 3 50
python cli.py acad add_disciplina 1002 "Matemática" 3 50  
python cli.py acad add_disciplina 1001 "Fundamentos de Programação" 4 60 --prereq "Matemática"  
python cli.py acad add_disciplina 1001 "Estrutura de Dados" 3 45 --prereq "Fundamentos de Programação"  
python cli.py acad add_disciplina 1003 "Mecânica dos Fluidos" 4 80 
python cli.py acad add_disciplina 1004 "Genética" 3 40 
python cli.py acad add_disciplina 1005 "História do Brasil" 2 30 --semestre 1  
python cli.py acad add_disciplina 1006 "Mecânica Clássica" 3 50 --prereq "Física"  
python cli.py acad add_turma "Fundamentos de Programação" 2024.1 30 30/09/2024 --horario "SEG 18:00-20:00" --local "Sala 101"  
python cli.py acad add_turma "Estrutura de Dados" 2024.1 25 30/09/2024 --horario "TER 18:00-20:00" --local "Sala 102"  
python cli.py acad add_turma "Mecânica dos Fluidos" 2024.2 20 15/10/2024 --horario "QUA 18:00-20:00" --local "Laboratório de Engenharia"  
python cli.py acad add_turma "Genética" 2024.1 22 30/09/2024 --horario "SEG 18:00-20:00" --local "Auditório Principal"  
python cli.py acad add_turma "História do Brasil" 2024.1 18 10/10/2024 --horario "QUA 18:00-20:00" --local "Sala 205"  
python cli.py acad add_turma "Mecânica Clássica" 2024.1 24 15/10/2024 --horario "SEG 20:00-22:00" --local "Sala 110"  
python cli.py acad add_aluno "Alice Silva" "alice@example.com" 1001  
python cli.py acad add_aluno "Bruno Oliveira" "bruno@example.com" 1002  
python cli.py acad add_aluno "Carla Souza" "carla@example.com" 1003  
python cli.py acad add_aluno "Diego Fernandes" "diego@example.com" 1004  
python cli.py acad add_aluno "Eduarda Costa" "eduarda@example.com" 1005  
python cli.py acad add_aluno "Felipe Lima" "felipe@example.com" 1006  
python cli.py acad matricular 1 "1"  # Matricula Alice na turma "Fundamentos de Programação" (ID 1)  
python cli.py acad matricular 2 "1"  # Matricula Bruno na turma "Fundamentos de Programação"  
python cli.py acad matricular 3 "3"  # Matricula Carla na turma "Mecânica dos Fluidos" (ID 3)  
python cli.py acad matricular 4 "4"  # Matricula Diego na turma "Genética" (ID 4)  
python cli.py acad matricular 5 "5"  # Matricula Eduarda na turma "História do Brasil" (ID 5)  
python cli.py acad matricular 6 "6"  # Matricula Felipe na turma "Mecânica Clássica" (ID 6)


# Editar e-mail de um aluno  
#edit_aluno --email "alice_nova@example.com" 1  

# Remover um curso  
#del_curso 1006  

# Listar todos os cursos  
#list_cursos  

# Buscar aluno por matrícula  
#busc_aluno 1  

# Trancar disciplina de um aluno  
#trancar_disciplina 1 "1"  

# Lançar nota de uma avaliação  
#lancar_nota 1 "1" "AB1" 7.5  

# Lançar frequência de uma aula  
#lancar_frequencia 1 "1" "10/10/2024" "presente"  

# Concluir disciplina (turma)  
#concluir "1"  

