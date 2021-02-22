# Indices:
TAMANHO = 0
FREQUENCIA = 1
GANHO = 2


def obtem_anuncio(lista_parametro):
    tamanho = int(lista_parametro[0])
    frequencia = int(lista_parametro[1])
    ganho = tamanho * frequencia
    return [tamanho, frequencia, ganho]
