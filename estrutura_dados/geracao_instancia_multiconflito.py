import csv
import os
import random as rd


def gera_instancia(nome,
                   tamanho_quadro,
                   quantidade_quadros,
                   quantidade_anuncio,
                   lista_tamanho_frequencia,
                   porcentagem_conflito
                   ):

    local = f'instancias/Multiconflito/{nome}_{round(porcentagem_conflito * 100)}'
    if not os.path.exists(local):
        os.mkdir(local)

    gera_ambiente(local, tamanho_quadro, quantidade_quadros)
    print('Ambiente gerado')

    salva_matriz_anuncios(local, lista_tamanho_frequencia)
    print('Anúncios gerados')

    gera_conflito(local, quantidade_anuncio, porcentagem_conflito)
    print('Conflitos gerados')


def salva_matriz_anuncios(local, lista_tamanho_frequencia):
    arquivo = open(f'{local}/anuncios.csv', 'w+')
    arquivo_csv = csv.writer(arquivo)
    arquivo_csv.writerows(lista_tamanho_frequencia)
    arquivo.close()


def gera_ambiente(local, tamanho_quadro, quantidade_quadros):
    arquivo = open(f'{local}/ambiente.csv', 'w+')
    arquivo_csv = csv.writer(arquivo)
    arquivo_csv.writerow(['tamanho-quadro', 'quantidade-quadros'])
    arquivo_csv.writerow([tamanho_quadro, quantidade_quadros])
    arquivo.close()


def gera_matriz_anuncios(quantidade_anuncios, tamanho_min, tamanho_max, frequencia_min, frequencia_max):
    lista_tamanho_frequencia = [[0, 0]] * quantidade_anuncios
    for i in range(quantidade_anuncios):
        tamanho = rd.randint(tamanho_min, tamanho_max)
        frequencia = rd.randint(frequencia_min, frequencia_max)
        lista_tamanho_frequencia[i] = [tamanho, frequencia]
    return lista_tamanho_frequencia


def gera_conflito(local, quantidade_anuncios, porcentagem_conflito):
    arquivo = open(f'{local}/conflitos.csv', 'w+')
    arquivo_csv = csv.writer(arquivo)
    for i in range(quantidade_anuncios):
        linha_conflito = [0] * (i + 1)
        for j in range(i):
            linha_conflito[j] = int(rd.random() < porcentagem_conflito)
        arquivo_csv.writerow(linha_conflito)
    arquivo.close()


def gera_grupo_aleatorio_medio():

    A = 500
    K = 250
    L = 100
    W = 30
    lista_C = [0.1, 0.3, 0.5, 0.7]

    tamanho_quadro = L
    quantidade_quadros = K
    quantidade_anuncio = A
    tamanho_min = 1
    tamanho_max = L
    frequencia_min = 1
    frequencia_max = W

    rd.seed(1)

    lista_tamanho_frequencia = gera_matriz_anuncios(quantidade_anuncio, tamanho_min, tamanho_max, frequencia_min, frequencia_max)

    for C in lista_C:
        print('\nInstancia medio', C)
        gera_instancia('multiconflito', tamanho_quadro, quantidade_quadros, quantidade_anuncio, lista_tamanho_frequencia, C)


gera_grupo_aleatorio_medio()
