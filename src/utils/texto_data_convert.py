from datetime import datetime
def texto_para_data_load_settings(texto):
    #Retorna objeto comparável
    data = datetime.strptime(texto, "%Y-%m-%d").date()
    return data

def data_para_texto(data):
    #Retorna o texto da data
    if hasattr(data, "strftime"):
        texto = data.strftime("%Y-%m-%d")
    elif "/" in data:
        texto = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
    else:
        texto = data
    return texto


def inversor_texto_data(texto):
    #Retorna o texto
    return datetime.strptime(texto, "%Y-%m-%d").strftime("%d/%m/%Y")
