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

    local = f'instancias/Aleatorio/{nome}'
    if not os.path.exists(local):
        os.mkdir(local)

    gera_ambiente(local, tamanho_quadro, quantidade_quadros)
    print('Ambiente gerado')

    gera_anuncios(local, quantidade_anuncio, tamanho_min,
                  tamanho_max, frequencia_min, frequencia_max)
    print('Anúncios gerados')

    gera_conflito(local, quantidade_anuncio, porcentagem_conflito)
    print('Conflitos gerados')


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


def gera_basico_pequeno(indice='00', seed=1):
    A = 100
    K = 75
    L = 50
    W = 30
    C = 0.3
    gera_instancia(f'aleatorio_pequeno_{indice}',
                   tamanho_quadro=L,
                   quantidade_quadros=K,
                   quantidade_anuncio=A,
                   tamanho_min=1,
                   tamanho_max=L,
                   frequencia_min=1,
                   frequencia_max=W,
                   porcentagem_conflito=C,
                   seed=seed)


def gera_basico_medio(indice='00', seed=1):
    A = 500
    K = 250
    L = 100
    W = 30
    C = 0.3
    gera_instancia(f'aleatorio_medio_{indice}',
                   tamanho_quadro=L,
                   quantidade_quadros=K,
                   quantidade_anuncio=A,
                   tamanho_min=1,
                   tamanho_max=L,
                   frequencia_min=1,
                   frequencia_max=W,
                   porcentagem_conflito=C,
                   seed=seed)


def gera_basico_grande(indice='00', seed=1):
    A = 1000
    K = 500
    L = 250
    W = 30
    C = 0.4
    gera_instancia(f'aleatorio_grande_{indice}',
                   tamanho_quadro=L,
                   quantidade_quadros=K,
                   quantidade_anuncio=A,
                   tamanho_min=1,
                   tamanho_max=L,
                   frequencia_min=1,
                   frequencia_max=W,
                   porcentagem_conflito=C,
                   seed=seed)


def gera_basico_gigante(indice='00', seed=1):
    A = 10000
    K = 500
    L = 200
    W = 30
    C = 0.4
    gera_instancia(f'aleatorio_gigante_{indice}',
                   tamanho_quadro=L,
                   quantidade_quadros=K,
                   quantidade_anuncio=A,
                   tamanho_min=1,
                   tamanho_max=L,
                   frequencia_min=1,
                   frequencia_max=W,
                   porcentagem_conflito=C,
                   seed=seed)


def gera_grupo_aleatorio_pequeno(quantidade=20):
    for i in range(quantidade):
        print('\nInstancia', i)
        indice = str(i).zfill(2)
        gera_basico_pequeno(indice, seed=i)


def gera_grupo_aleatorio_medio(quantidade=20):
    for i in range(quantidade):
        print('\nInstancia', i)
        indice = str(i).zfill(2)
        gera_basico_medio(indice, seed=i)


def gera_grupo_aleatorio_grande(quantidade=20):
    for i in range(quantidade):
        print('\nInstancia', i)
        indice = str(i).zfill(2)
        gera_basico_grande(indice, seed=i)


def gera_grupo_aleatorio_gigante(quantidade=20):
    for i in range(quantidade):
        print('\nInstancia', i)
        indice = str(i).zfill(2)
        gera_basico_gigante(indice, seed=i)


def gera_todas_instancias(quantidade=20):
    gera_grupo_aleatorio_pequeno(quantidade)
    gera_grupo_aleatorio_medio(quantidade)
    gera_grupo_aleatorio_grande(quantidade)
    gera_grupo_aleatorio_gigante(quantidade)
