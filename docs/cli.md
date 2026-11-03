# Guia de uso da CLI do SGCA

Este guia mostra como usar o `cli.py`

## Estrutura do Guia
- Visão geral 
- Lista de comandos 
- Comandos não aceitos e erros de formato

## Como rodar

Todos os comandos seguem o mesmo formato:

`python cli.py acad <comando> <argumentos>`

A palavra `acad` é obrigatória e vem sempre antes do comando como nas especificações. Para ver a ajuda, use `-h` depois do comando acad, 
o programa funciona executando o cli.py em sua pasta padrão, verifique se os arquivos estão na estrutura correta do github:

```bash
python cli.py acad -h                 # lista todos os comandos
python cli.py acad add_turma -h       # mostra os argumentos de um comando
```

Se o valor tiver espaço, coloque entre aspas: `"Ciência da Computação"`.

### Onde fica o banco de dados

Por padrão, a CLI usa o arquivo `data/sgca.db`, e esse caminho é relativo à pasta de onde você roda o comando. Por isso, para o banco ficar em `../src/data/sgca.db`, rode de dentro de `src`:

```bash
cd src
python cli.py acad list_cursos
```

Para usar outro arquivo de banco (útil para testes ou para não mexer nos dados reais), passe `--db` **antes** de `acad`:

```bash
python src/cli.py --db /tmp/teste.db acad list_cursos
```

## Passo a passo: do zero até a nota final

O exemplo abaixo monta um curso pequeno, matricula um aluno e termina a disciplina. Siga na ordem, porque cada passo depende do anterior.

**1. Criar o curso** (código entre 1000 e 9999, nome, carga horária):

```bash
python cli.py acad add_curso 1001 "Ciência da Computação" 3600
```

**2. Criar as disciplinas** (código do curso, nome, créditos, carga horária). Se uma disciplina exige outra antes, use `--prereq` com o nome da disciplina exigida:

```bash
python cli.py acad add_disciplina 1001 "Matemática" 3 50
python cli.py acad add_disciplina 1001 "Fundamentos de Programação" 4 60 --prereq "Matemática"
```

Pode repetir `--prereq` para mais de um pré-requisito. Também existe `--semestre` para indicar em qual semestre do curso a disciplina costuma ser cursada.

**3. Abrir uma turma** (nome da disciplina, semestre, vagas, data limite de matrícula):

```bash
python cli.py acad add_turma "Matemática" 2026.1 30 30/09/2026 --horario "SEG 18:00-20:00" --local "Sala 101"
```

`--horario` pode ser repetido se a turma tiver mais de um encontro na semana (por exemplo, `--horario "SEG 18:00-20:00" --horario "QUA 18:00-20:00"`). As turmas recebem um ID em sequência; é com esse ID que você as referencia nos próximos passos. Se tiver dúvida de qual é o ID, use `busc_turma` ou `list_alunos_turma`.

**4. Cadastrar o aluno** (nome, e-mail, código do curso):

```bash
python cli.py acad add_aluno "Alice Silva" alice@example.com 1001
```

A saída mostra o número de matrícula gerado, como `Criando Alice Silva (454334)`. Anote esse número, ele identifica o aluno daqui para frente.

**5. Matricular o aluno na turma** (matrícula, ID da turma):

```bash
python cli.py acad matricular 454334 1
```

**6. Lançar notas e presença:**

```bash
python cli.py acad lancar_nota 454334 1 AB1 8.5
python cli.py acad lancar_nota 454334 1 AB2 7
python cli.py acad lancar_frequencia 454334 1 15/10/2026 presente
```

Cada nota lançada devolve a média atual. A frequência devolve o percentual de presença até aquele momento. O nome da avaliação (`AB1`, `AB2`) é livre, 
podem até ser usados números.
```bash 
python cli.py acad lancar_nota 454334 1 1 7
```
Esse comando é equivalente à lançar a nota do aluno com Nº 454334 na turma 1, na primeira avaliação com nota 7.

**7. Encerrar a turma:**

```bash
python src/cli.py acad concluir_disciplina 1
```

A turma é encerrada e a CLI lista a situação de cada aluno. Se quiser definir as regras de aprovação na hora, em vez de usar o padrão do sistema:

```bash
python src/cli.py acad concluir_disciplina 1 --nota_minima 6.0 --frequencia_minima 75
```

**8. Conferir o resultado:**

```bash
python src/cli.py acad hist_aluno 454334     # histórico do aluno
python src/cli.py acad top_nt 1              # ranking da turma
python src/cli.py acad top_nc 1001           # ranking do curso
```

## Referência dos comandos

### Cursos

| Comando | Argumentos | O que faz |
|---|---|---|
| `add_curso` | `cod_curso nome carga_horaria` | Cria um curso |
| `del_curso` | `cod_curso` | Remove um curso |
| `edit_curso` | `cod_curso [--nome] [--carga_horaria]` | Cria um curso |
| `list_cursos` | (nenhum) | Lista todos os cursos |
| `list_disciplinas_curso` | `cod_curso` | Lista as disciplinas do curso, com créditos e pré-requisitos |
| `list_alunos_curso` | `cod_curso` | Lista os alunos do curso com a matrícula de cada um |

### Disciplinas e turmas

| Comando | Argumentos | O que faz |
|---|---|---|
| `add_disciplina` | `cod_curso nome creditos carga_horaria [--prereq NOME]... [--semestre N]` | Cria uma disciplina dentro de um curso |
| `add_turma` | `disciplina semestre vagas data_limite [--horario H]... [--local L]` | Abre uma turma para a disciplina. A data é `dd/mm/aaaa` |
| `busc_turma` | `id_turma` | Mostra os dados da turma |
| `del_turma` | `id_turma` | Remove a turma |
| `list_alunos_turma` | `id_turma` | Mostra vagas ocupadas, status da turma e os alunos matriculados |
| `mudar_status_turma` | `id_turma` | Alterna a turma entre Aberta e Fechada. Ao **fechar**, todos os alunos são removidos da turma e a CLI informa quantos saíram |

### Alunos

| Comando | Argumentos | O que faz |
|---|---|---|
| `add_aluno` | `nome email cod_curso` | Cadastra o aluno e gera a matrícula |
| `edit_aluno` | `matricula [--nome N] [--email E]` | Altera nome e/ou e-mail |
| `del_aluno` | `matricula` | Remove o aluno |
| `busc_aluno` | `matricula` | Mostra matrícula, nome, e-mail, curso, CR e status do curso |

### Matrícula, notas e frequência

| Comando | Argumentos | O que faz |
|---|---|---|
| `matricular` | `matricula id_turma` | Matricula o aluno em uma turma |
| `lancar_nota` | `matricula id_turma avaliacao nota` | Lança uma nota de 0 a 10 e devolve a média atual |
| `lancar_frequencia` | `matricula id_turma data presente\|falta` | Registra presença ou falta numa data (`dd/mm/aaaa`) e devolve a frequência atual |
| `concluir_disciplina` | `id_turma [--nota_minima X] [--frequencia_minima Y]` | Encerra a turma, grava o histórico e mostra a situação de cada aluno. Sem as opções, usa os valores padrão do sistema |

### Trancamento

| Comando | Argumentos | O que faz |
|---|---|---|
| `trancar_disciplina` | `matricula id_turma` | Tira o aluno daquela turma (as vagas ocupadas diminuem em 1) e registra a matrícula no histórico com status `Trancada` |
| `trancar_curso` | `matricula` | Faz o mesmo com **todas** as matrículas em andamento (status `Cursando`) do aluno e muda o status do curso dele para `Trancado`. A partir daí ele não consegue mais se matricular |

Disciplinas que o aluno já concluiu não são afetadas pelo trancamento do curso. Elas continuam no histórico com o resultado que tiveram.

### Relatórios

| Comando | Argumentos | O que faz |
|---|---|---|
| `top_nt` | `id_turma` | Ranking dos alunos da turma pela média. Enquanto a turma não for encerrada, aparece como "Média temporária" |
| `top_nc` | `cod_curso` | Ranking dos alunos do curso pelo CR |
| `hist_aluno` | `matricula` | Histórico do aluno: disciplina, semestre, créditos, nota, status e data de conclusão |

## Quando uma matrícula é negada

O sistema recusa a matrícula nestes casos:

- O aluno ainda não cumpriu o pré-requisito da disciplina.
- O horário da turma bate com o de outra turma em que o aluno já está matriculado. Horários encostados, como `SEG 18:00-20:00` e `SEG 20:00-22:00`, não contam como choque.
- A turma está lotada.
- O curso do aluno está trancado.

Nesses casos a CLI imprime uma linha começando com `Erro:` e encerra com código 1. Em scripts, dá para testar isso direto:

```bash
python cli.py acad matricular 454334 3 || echo "matrícula negada"
```

## Pontos de atenção

- A ordem dos comandos importa: criar curso, depois disciplinas, depois turmas, depois alunos, e só então matricular. Se algo falhar no meio, confira o `Erro:` impresso antes de repetir o comando.

- **Frequência mínima é um número inteiro**, enquanto a nota mínima aceita decimais (`--nota_minima 6.5` funciona, `--frequencia_minima 82.5` não).
