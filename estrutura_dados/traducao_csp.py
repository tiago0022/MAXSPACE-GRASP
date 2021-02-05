import math
import os
import random as rd

from pandas import DataFrame

from geracao_instancia import gera_ambiente, gera_conflito

CAMINHO_ENTRADA_FALKENAUER_U = 'instancias_csp/Falkenauer_U/'
CAMINHO_SAIDA_FALKENAUER_U = 'instancias/Falkenauer_U/'

CAMINHO_ENTRADA_FALKENAUER_T = 'instancias_csp/Falkenauer_T/'
CAMINHO_SAIDA_FALKENAUER_T = 'instancias/Falkenauer_T/'

def arquivo_texto_para_matriz(caminho):
    arquivo = open(caminho, "r")
    matriz = []
    for linha in arquivo:
        matriz.append(list(map(int, linha.strip('\n').split('\t'))))
    arquivo.close()
    return matriz

def gera_instancia_falkenauer_u(nome_arquivo:str, seed=1):

    rd.seed(seed)

    caminho_nova_pasta = CAMINHO_SAIDA_FALKENAUER_U + nome_arquivo.strip('.txt').lower()
    if not os.path.exists(caminho_nova_pasta):
        os.mkdir(caminho_nova_pasta)

    matriz = arquivo_texto_para_matriz(CAMINHO_ENTRADA_FALKENAUER_U + nome_arquivo)
    
    gera_ambiente_falkenauer_u(caminho_nova_pasta, matriz)
    gera_anuncios_csp(caminho_nova_pasta, matriz)
    gera_conflito_csp(caminho_nova_pasta, matriz)


def gera_instancia_falkenauer_t(nome_arquivo:str, seed=1):

    rd.seed(seed)

    caminho_nova_pasta = CAMINHO_SAIDA_FALKENAUER_T + nome_arquivo.strip('.txt').lower()
    if not os.path.exists(caminho_nova_pasta):
        os.mkdir(caminho_nova_pasta)

    matriz = arquivo_texto_para_matriz(CAMINHO_ENTRADA_FALKENAUER_T + nome_arquivo)
    
    gera_ambiente_falkenauer_t(caminho_nova_pasta, matriz)
    gera_anuncios_csp(caminho_nova_pasta, matriz)
    gera_conflito_csp(caminho_nova_pasta, matriz)
    
    
def gera_ambiente_falkenauer_u(local, matriz):
    tamanho_quadro = matriz[1][0]
    quantidade_quadro = obtem_quantidade_quadro_falkenauer_u(matriz)
    gera_ambiente(local, tamanho_quadro, quantidade_quadro)


def gera_ambiente_falkenauer_t(local, matriz):
    tamanho_quadro = matriz[1][0]
    quantidade_quadro = obtem_quantidade_quadro_falkenauer_t(matriz)
    gera_ambiente(local, tamanho_quadro, quantidade_quadro)


def obtem_quantidade_quadro_falkenauer_u(matriz):
    I = matriz[0][0]
    L = matriz[1][0]
    soma = 0
    maior_d = 0
    for i in range(2, I + 2):
        h = matriz[i][0]
        d = matriz[i][1]
        elemento = (h * d) / (2 * L)
        soma = soma + elemento
        if d > maior_d:
            maior_d = d
    soma = math.ceil(soma)
    if maior_d > soma:
        return maior_d
    return soma


def obtem_quantidade_quadro_falkenauer_t(matriz):
    I = matriz[0][0]
    soma = 0
    for i in range(2, I + 2):
        d = matriz[i][1]
        soma = soma + (d / 3)
    return int(soma)


def gera_anuncios_csp(local, matriz):
    quantidade_anuncios = matriz[0][0]
    df_anuncio = DataFrame(columns=['indice', 'tamanho', 'frequencia'])
    for i in range(quantidade_anuncios):
        indice = i + 1
        tamanho = matriz[i + 2][0]
        frequencia = matriz[i + 2][1]
        df_anuncio = df_anuncio.append({'indice': indice, 'tamanho': tamanho, 'frequencia': frequencia}, ignore_index=True)
    df_anuncio.set_index('indice', inplace=True)
    df_anuncio.to_csv(f'{local}/anuncios.csv')


def gera_conflito_csp(local, matriz):
    quantidade_anuncios = matriz[0][0]
    porcentagem_conflito = 0.3 if quantidade_anuncios <= 500 else 0.4
    gera_conflito(local, quantidade_anuncios, porcentagem_conflito)


def gera_todos_falkenauer_t(seed=1):
    lista_grupo = ['60', '120', '249', '501']
    for grupo in lista_grupo:
        for i in range(20):
            indice = str(i).zfill(2)
            nome_arquivo = f'Falkenauer_t{grupo}_{indice}.txt'
            gera_instancia_falkenauer_t(nome_arquivo, seed=seed)
        print(f'Fim do grupo T {grupo}')
    print('Fim de Falkenauer T')

def gera_todos_falkenauer_u(seed=1):
    lista_grupo = ['120', '250', '500', '1000']
    for grupo in lista_grupo:
        for i in range(20):
            indice = str(i).zfill(2)
            nome_arquivo = f'Falkenauer_u{grupo}_{indice}.txt'
            gera_instancia_falkenauer_u(nome_arquivo, seed=seed)
        print(f'Fim do grupo U {grupo}')
    print('Fim de Falkenauer U')

    