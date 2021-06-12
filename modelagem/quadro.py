from tempo_execucao import RegistroTempo

from modelagem.anuncio import TAMANHO

# Indices
ESPACO_OCUPADO = 0
LISTA_INDICE_ANUNCIO = 1


def pode_ser_inserido(quadro, anuncio, indice_anuncio, matriz_conflito, tamanho_quadro, espaco_liberado=0, anuncio_liberado=None) -> bool:

    tempo = RegistroTempo('Verificar se pode inserir')

    tamanho_anuncio = anuncio[TAMANHO]
    espaco_ocupado = quadro[ESPACO_OCUPADO] - espaco_liberado
    lista_indice_anuncio_inserido = quadro[LISTA_INDICE_ANUNCIO]

    if espaco_ocupado + tamanho_anuncio > tamanho_quadro:
        # tempo.exibe()
        return False

    if existe_conflito(matriz_conflito, indice_anuncio, lista_indice_anuncio_inserido, anuncio_liberado):
        # tempo.exibe()
        return False

    # tempo.exibe()
    return True


def existe_conflito(matriz_conflito, indice_anuncio, lista_indice_anuncio_inserido, anuncio_liberado=None):
    for indice_anuncio_inserido in lista_indice_anuncio_inserido:
        if indice_anuncio < indice_anuncio_inserido:
            if matriz_conflito[indice_anuncio_inserido][indice_anuncio] and indice_anuncio_inserido != anuncio_liberado:
                return True
        elif matriz_conflito[indice_anuncio][indice_anuncio_inserido] and indice_anuncio_inserido != anuncio_liberado:
            return True
        elif indice_anuncio == indice_anuncio_inserido:
            return True
    return False
