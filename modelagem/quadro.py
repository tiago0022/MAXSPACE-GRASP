from pandas.core.frame import DataFrame
from pandas.core.series import Series


def pode_ser_inserido(quadro: Series, anuncio: DataFrame, df_conflito, tamanho_quadro) -> bool:

    indice_anuncio = anuncio.first_valid_index()
    tamanho_anuncio = anuncio['tamanho'].values[0]

    espaco_ocupado = quadro['espaco_ocupado']
    lista_indice_anuncio_inserido = quadro['lista_indice_anuncio']

    if espaco_ocupado + tamanho_anuncio > tamanho_quadro:
        return False

    if existe_conflito(df_conflito, indice_anuncio, lista_indice_anuncio_inserido):
        return False

    return True


def existe_conflito(df_conflito: DataFrame, indice_anuncio, lista_indice_anuncio_inserido):
    for indice_anuncio_inserido in lista_indice_anuncio_inserido:
        if df_conflito[str(indice_anuncio_inserido)][indice_anuncio]:
            return True
    return False
