import csv
import os
import random as rd


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
    arquivo = open(f'{local}/ambiente.csv', 'w+')
    arquivo_csv = csv.writer(arquivo)
    arquivo_csv.writerow(['tamanho-quadro', 'quantidade-quadros'])
    arquivo_csv.writerow([tamanho_quadro, quantidade_quadros])
    arquivo.close()


def gera_anuncios(local, quantidade_anuncios, tamanho_min, tamanho_max, frequencia_min, frequencia_max):
    lista_tamanho_frequencia = [[0, 0]] * quantidade_anuncios
    for i in range(quantidade_anuncios):
        tamanho = rd.randint(tamanho_min, tamanho_max)
        frequencia = rd.randint(frequencia_min, frequencia_max)
        lista_tamanho_frequencia[i] = [tamanho, frequencia]
    arquivo = open(f'{local}/anuncios.csv', 'w+')
    arquivo_csv = csv.writer(arquivo)
    arquivo_csv.writerow(['tamanho', 'frequencia'])
    arquivo_csv.writerows(lista_tamanho_frequencia)
    arquivo.close()


def gera_conflito(local, quantidade_anuncios, porcentagem_conflito):
    arquivo = open(f'{local}/conflitos.csv', 'w+')
    arquivo_csv = csv.writer(arquivo)
    for i in range(quantidade_anuncios):
        linha_conflito = [0] * (i + 1)
        for j in range(i):
            linha_conflito[j] = int(rd.random() < porcentagem_conflito)
        arquivo_csv.writerow(linha_conflito)
    arquivo.close()


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


# gera_todas_instancias()
