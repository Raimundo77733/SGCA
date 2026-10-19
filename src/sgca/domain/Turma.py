from src.sgca.domain.Oferta import Oferta
from src.sgca.errors.Validation import HorarioInvalidoError


def _hora_em_minutos(texto):
    """'18:30' -> 1110"""
    hora, minuto = texto.split(":")
    return int(hora) * 60 + int(minuto)


def _converter_horario(texto):
    """'SEG 18:00-20:00' -> ('SEG', 1080, 1200)"""
    mensagem = f"Horário inválido: '{texto}'. Use o formato 'SEG 18:00-20:00'."
    try:
        dia, faixa = texto.strip().split()
        inicio, fim = faixa.split("-")
        inicio = _hora_em_minutos(inicio)
        fim = _hora_em_minutos(fim)
    except (ValueError, AttributeError):
        raise HorarioInvalidoError(mensagem)
    if not 0 <= inicio < fim <= 24 * 60:
        raise HorarioInvalidoError(mensagem)
    return dia.upper(), inicio, fim


class Turma(Oferta):

    def __init__(self, horarios, vagas_max, id_disciplina, semestre, data_limite):
        super().__init__(semestre, data_limite)
        self.id_disciplina = id_disciplina
        # dados da disciplina: preenchidos pelo repositório ao ler do banco
        self.nome_disciplina = ""
        self.cod_curso = ""
        self.nome_curso = ""
        self.carga_horaria = 0
        self.creditos = 0
        self.horarios = horarios
        self.intervalos()  # valida o formato dos horários logo na criação
        self.vagas_max = vagas_max
        self.inscritos=0
        self.id_turma =0
        self.status = "Aberta"
        self.local = ""


    def __len__(self):
        return self.inscritos

    def intervalos(self):
        """Horários em tuplas comparáveis: [('SEG', 1080, 1200), ...], por causa da conversão em minutos"""
        lista = []
        for texto in self.horarios.values():
            lista.append(_converter_horario(texto))
        return lista

    def tem_choque_com(self, outra):
        """True se algum intervalo coincide com o de outra turma."""
        for dia, inicio, fim in self.intervalos():
            #Itera sobre dia,inicio em minutos,fim em minutos
            for outro_dia, outro_inicio, outro_fim in outra.intervalos():
                #compara com a self.intervalos de outra turma
                if dia == outro_dia and inicio < outro_fim and outro_inicio < fim:
                    #Condição de choque, é no mesmo dia, o fim de aula de uma turmaA se sobrepões ao começo da outra B em minutos
                    #ou o oposto fim B>A
                    return True
        return False

    def __str__(self):
        texto = (f"ID:{self.id_turma}\nNome da Disciplina:{self.nome_disciplina}\n"
                 f"Status:{self.status}\nInscritos:{self.inscritos}/{self.vagas_max}\nHorários:")
        for horario in self.horarios.values():
            texto += f"\n{horario}"
        return texto
