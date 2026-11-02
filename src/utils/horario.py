from errors import HorarioInvalidoError

def hora_em_minutos(texto):
    """'18:30' -> 1110"""
    hora, minuto = texto.split(":")
    return int(hora) * 60 + int(minuto)


def converter_horario(texto):
    """'SEG 18:00-20:00' -> ('SEG', 1080, 1200)"""
    mensagem = f"Horário inválido: '{texto}'. Use o formato 'SEG 18:00-20:00'."
    try:
        dia, faixa = texto.strip().split()
        inicio, fim = faixa.split("-")
        inicio = hora_em_minutos(inicio)
        fim = hora_em_minutos(fim)
    except (ValueError, AttributeError):
        raise HorarioInvalidoError(mensagem)
    if not 0 <= inicio < fim <= 24 * 60:
        raise HorarioInvalidoError(mensagem)
    return dia.upper(), inicio, fim
