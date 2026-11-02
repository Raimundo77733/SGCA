from errors import JaExisteError,IntegridadeError

def determinar_tipo_erro(erro):
    texto = str(erro)
    if "UNIQUE" in texto or "PRIMARY KEY" in texto:
        #Caso haja tentativa de gravar dados sobre uma chave única
        return JaExisteError("Já existe um registro com esses dados.")
    if "FOREIGN KEY" in texto:
        #Caso as chaves sejam inválidas ou haja problemas de alinhamento entre o banco e os objetos
        return IntegridadeError(
            "Operação inválida: o registro referencia algo inexistente "
            "ou ainda é referenciado por outros registros.")
    return IntegridadeError(f"Violação de integridade: {texto}")
    #Caso genérico em que o tipo de erro viola a integridade, mas não tem relação com a chave única ou estrangeira