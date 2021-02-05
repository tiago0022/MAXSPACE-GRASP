from typing import List, Tuple

import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.core.frame import DataFrame, Series


def obtemInstancia(caminhoInstancia: str) -> Tuple[DataFrame, DataFrame, DataFrame]:

    dfAmbiente = pd.read_csv(caminhoInstancia + '/ambiente.csv')
    dfAnuncio = pd.read_csv(caminhoInstancia + '/anuncios.csv', index_col='indice')
    dfConflito = pd.read_csv(caminhoInstancia + '/conflitos.csv', index_col='indice/indice')

    validaEntrada(dfAmbiente, dfAnuncio, dfConflito)

    return dfAnuncio, dfConflito, dfAmbiente["tamanho-quadro"][0], dfAmbiente["quantidade-quadros"][0]


def validaEntrada(dfAmbiente: DataFrame, dfAnuncio: DataFrame, dfConflito: DataFrame):
    
    validaDfAmbiente(dfAmbiente)
    validaDfAnuncio(dfAnuncio)
    validaDfConflito(dfConflito)

    if not (dfAnuncio.index == dfConflito.index).all():
        raise Exception("Tabela de conflitos está com índices diferentes dos anúncios")


def validaDfAmbiente(dfAmbiente: DataFrame):

    tamanhoQuadro = int(dfAmbiente["tamanho-quadro"][0])
    quantidadeQuadros = int(dfAmbiente["quantidade-quadros"][0])

    if tamanhoQuadro <= 0:
        raise Exception('Tamanho de quadro inválido')

    if quantidadeQuadros <= 0:
        raise Exception('Quantidade de quadros inválida')


def validaDfAnuncio(dfAnuncio: DataFrame):

    if len(dfAnuncio) <= 0:
        raise Exception('Quantidade de anúncios inválida')

    listaTamanho = dfAnuncio["tamanho"]
    listaFrequencia = dfAnuncio["frequencia"]

    if any(listaTamanho <= 0) or not is_integer_dtype(listaTamanho):
        raise Exception('Tamanho de anúncio inválido')

    if any(listaFrequencia <= 0) or not is_integer_dtype(listaFrequencia):
        raise Exception('Frequencia de anúncio inválido')


def validaDfConflito(dfConflito: DataFrame):

    if len(dfConflito) <= 0:
        raise Exception('Quantidade de conflitos inválida')

    if len(dfConflito) != len(dfConflito.columns):
        raise Exception(
            'Tabela de conflitos possui número diferente de linhas e colunas')

    if not (dfConflito.values == dfConflito.values.T).all():
        raise Exception('Tabela de conflitos está ambígua')

    if not (dfConflito.columns.astype(str) == dfConflito.index.astype(str)).all():
        raise Exception('Tabela de conflitos está com índices errados')
