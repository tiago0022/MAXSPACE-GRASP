from pandas import DataFrame


def calcula_ganho(df_anuncio: DataFrame):
    df_anuncio['ganho'] = df_anuncio['tamanho'] * df_anuncio['frequencia']
    return df_anuncio
