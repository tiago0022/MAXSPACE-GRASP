import os
import random as rd

import numpy as np
from pandas import DataFrame


def gera_instancia(nome,
                   tamanho_quadro,
                   quantidade_quadros,
                   quantidade_anuncio,
                   tamanho_min,
                   tamanho_max,
                   frequencia_min,
                   frequencia_max,
                   porcentagem_conflito,
                   seed=1):

    rd.seed(seed)

    local = f'instancias/{nome}'
    if not os.path.exists(local):
        os.mkdir(local)

    gera_ambiente(local, tamanho_quadro, quantidade_quadros)

    gera_anuncios(local, quantidade_anuncio, tamanho_min,
                  tamanho_max, frequencia_min, frequencia_max)

    gera_conflito(local, quantidade_anuncio, porcentagem_conflito)


def gera_ambiente(local, tamanho_quadro, quantidade_quadros):
    df_ambiente = DataFrame(columns=['tamanho-quadro', 'quantidade-quadros'])
    df_ambiente = df_ambiente.append(
        {'tamanho-quadro': tamanho_quadro, 'quantidade-quadros': quantidade_quadros}, ignore_index=True)
    df_ambiente.to_csv(f'{local}/ambiente.csv', index=False)


def gera_anuncios(local, quantidade_anuncios, tamanho_min, tamanho_max, frequencia_min, frequencia_max):
    df_anuncio = DataFrame(columns=['indice', 'tamanho', 'frequencia'])
    for i in range(quantidade_anuncios):
        indice = i + 1
        tamanho = rd.randint(tamanho_min, tamanho_max)
        frequencia = rd.randint(frequencia_min, frequencia_max)
        df_anuncio = df_anuncio.append(
            {'indice': indice, 'tamanho': tamanho, 'frequencia': frequencia}, ignore_index=True)
    df_anuncio.set_index('indice', inplace=True)
    df_anuncio.to_csv(f'{local}/anuncios.csv')


def gera_conflito(local, quantidade_anuncios, porcentagem_conflito):
    matriz_conflito = np.zeros(
        (quantidade_anuncios, quantidade_anuncios), dtype=int)
    for i in range(quantidade_anuncios):
        for j in range(i):
            conflito = int(rd.random() < porcentagem_conflito)
            matriz_conflito[i][j] = conflito
            matriz_conflito[j][i] = conflito
    df_conflito = DataFrame(
        matriz_conflito, columns=range(1, quantidade_anuncios + 1))
    df_conflito['indice/indice'] = range(1, quantidade_anuncios + 1)
    df_conflito.set_index('indice/indice', inplace=True)
    df_conflito.to_csv(f'{local}/conflitos.csv')


def gera_basico_pequeno(seed=1):
    gera_instancia('aleatorio_pequeno',
                   tamanho_quadro=50,
                   quantidade_quadros=75,
                   quantidade_anuncio=100,
                   tamanho_min=1,
                   tamanho_max=50,
                   frequencia_min=1,
                   frequencia_max=30,
                   porcentagem_conflito=0.3,
                   seed=seed)
