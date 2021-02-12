from typing import Tuple

import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.core.frame import DataFrame


def obtem_instancia(caminho_instancia: str) -> Tuple[DataFrame, DataFrame, DataFrame]:

    df_ambiente = pd.read_csv(caminho_instancia + 'ambiente.csv')
    df_anuncio = pd.read_csv(caminho_instancia + 'anuncios.csv', index_col='indice')
    df_conflito = pd.read_csv(caminho_instancia + 'conflitos.csv', index_col='indice/indice')

    valida_entrada(df_ambiente, df_anuncio, df_conflito)

    return df_anuncio, df_conflito, df_ambiente["tamanho-quadro"][0], df_ambiente["quantidade-quadros"][0]


def valida_entrada(df_ambiente: DataFrame, df_anuncio: DataFrame, df_conflito: DataFrame):

    valida_ambiente(df_ambiente)
    valida_anuncio(df_anuncio)
    valida_conflito(df_conflito)

    if (df_anuncio.index != df_conflito.index).all():
        raise Exception(
            "Tabela de conflitos está com índices diferentes dos anúncios")


def valida_ambiente(df_ambiente: DataFrame):

    tamanho_quadro = df_ambiente["tamanho-quadro"][0]
    quantidade_quadros = df_ambiente["quantidade-quadros"][0]

    if tamanho_quadro <= 0 or not is_integer_dtype(tamanho_quadro):
        raise Exception('Tamanho de quadro inválido')

    if quantidade_quadros <= 0 or not is_integer_dtype(quantidade_quadros):
        raise Exception('Quantidade de quadros inválida')


def valida_anuncio(df_anuncio: DataFrame):

    if len(df_anuncio) <= 0:
        raise Exception('Quantidade de anúncios inválida')

    lista_tamanho = df_anuncio["tamanho"]
    lista_frequencia = df_anuncio["frequencia"]

    if any(lista_tamanho <= 0) or not is_integer_dtype(lista_tamanho):
        raise Exception('Tamanho de anúncio inválido')

    if any(lista_frequencia <= 0) or not is_integer_dtype(lista_frequencia):
        raise Exception('Frequencia de anúncio inválido')


def valida_conflito(df_conflito: DataFrame):

    if len(df_conflito) <= 0:
        raise Exception('Quantidade de conflitos inválida')

    if len(df_conflito) != len(df_conflito.columns):
        raise Exception(
            'Tabela de conflitos possui número diferente de linhas e colunas')

    if (df_conflito.values != df_conflito.values.T).all():
        raise Exception('Tabela de conflitos está ambígua')

    if (df_conflito.columns.astype(str) != df_conflito.index.astype(str)).all():
        raise Exception('Tabela de conflitos está com índices errados')

    for linha in df_conflito.values:
        for item in linha:
            if item != 1 and item != 0:
                raise Exception('Tabela de conflitos possui valor inválido')
