# SGCA — Sistema de Gerenciamento de Cursos e Alunos

Sistema desenvolvido para avaliação acadêmica durante o curso de Engenharia de Software.

## Objetivo

O SGCA centralizará e organizará dados relacionados à administração de cursos e alunos, proporcionando maior controle sobre cadastros, matrículas e acompanhamento acadêmico.

## Funcionalidades

- Cadastro, edição e exclusão de alunos
- Cadastro e gerenciamento de cursos
- Controle de matrículas
- Consulta de alunos e cursos
- Gerenciamento de informações acadêmicas
- Controle de acesso por permissões de classe
- Relatórios de performance dos estudantes

## Tecnologias utilizadas

- **Backend:** `<python>`
- **Banco de dados:** `<Sqllite3>`
- **Testes:** `<pytest>`

## UML Textual

## Classes Base
1. Oferta (classe base para ofertas)
   - Subclasse: Turma

2. Pessoa (classe base para pessoas)
   - Subclasses
      - Aluno 
      - Secretaria
      - Professor

## Classes Principais
3. Turma (herda de Oferta)
   - Atributos: curso, id_turma, lista_alunos, semestre, horários, vagas_max, disciplina, pré-requisitos, carga_horária, tempo_limite_matricula, local, ementa, status
   - Métodos:
     - cadastrar_turma()
     - remover_turma()
     - editar_dados_turma()
     - listar_alunos()
     - calcular_taxa_de_aprovação()
     - mostrar_distribuição_de_notas()

4. Aluno (herda de Pessoa)
   - Atributos: nome, email, cod_curso, n_matricula, histórico, matrículas_ativas, matrículas_concluidas
   - Métodos:
     - calcular_cr()
     - mostrar_historico()
     - trancar_curso()
     - trancar_disciplina()

5. Secretaria (herda de Pessoa)
   - Métodos:
     - cadastrar_aluno()
     - editar_dados_aluno()
     - remover_aluno()

6. Professor (herda de Pessoa)
   - Atributos: nome, email, identificador, lista_turmas
   - Métodos:
     - lancar_nota()
     - lancar_frequencia()
     - calcular_situacao()

7. Curso
   - Atributos: nome_curso, cod_curso, disciplinas_do_curso, lista_alunos
   - Métodos:
     - listar_cursos()
     - criar_curso()
     - remover_curso()
     - editar_dados_curso()
     - relatorio_topn()
     - relatorio_risco()

8. Matricula (associa Aluno e Turma)
   - Atributos: aluno, turma, média, notas, frequência_media, registro_frequência, status, tempo_restante_trancamento
   - Métodos:
     - verificar_requisitos()
     - verificar_vagas()
     - verificar_choque_horario()

## Relacionamentos
- Turma contém objetos Aluno em lista_alunos
- Aluno possui objetos Matricula em matrículas_ativas e matrículas_concluidas
- Curso contém lista de objetos Alunos
- Professor está associado a objetos Turma via lista_turmas
- Matricula liga Aluno e Turma 


## Relação entre as classes
![Alt text](/UML/mermaid-diagram.png "Diagrama UML do projeto SGCA")