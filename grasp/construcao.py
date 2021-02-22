
import random as rd

from modelagem.ambiente import Ambiente
from modelagem.anuncio import FREQUENCIA, GANHO, TAMANHO
from modelagem.quadro import (ESPACO_OCUPADO, LISTA_INDICE_ANUNCIO,
                              pode_ser_inserido)
from pandas import DataFrame
from tempo_execucao import RegistroTempo

EXIBE_ITERACAO = 0  # Padrão = False


def constroi(matriz_anuncio, matriz_conflito, ambiente: Ambiente, aleatoriedade, seed=1):

    tempo = RegistroTempo('Construção')

    matriz_solucao = solucao_vazia(ambiente.quantidade_quadros)

    quantidade_anuncios = len(matriz_anuncio)
    lista_disponibilidade_anuncio = [1] * quantidade_anuncios

    exibe_iteracao(-1, matriz_anuncio, matriz_solucao, lista_disponibilidade_anuncio)

    for iteracao in range(quantidade_anuncios):

        menor_ganho, maior_ganho = obtem_menor_e_maior_ganhos_disponiveis(matriz_anuncio, quantidade_anuncios, lista_disponibilidade_anuncio)

        limite_inferior = maior_ganho - aleatoriedade * (maior_ganho - menor_ganho)

        lista_indice_candidato = obtem_lista_indice_anuncio_candidato(matriz_anuncio, limite_inferior, quantidade_anuncios, lista_disponibilidade_anuncio)
        indice_selecionado = escolhe_candidato(lista_indice_candidato)

        insere_first_fit(matriz_solucao, matriz_anuncio[indice_selecionado], indice_selecionado, matriz_conflito, ambiente)

        exibe_iteracao(iteracao, matriz_anuncio, matriz_solucao, lista_disponibilidade_anuncio, limite_inferior, lista_indice_candidato, indice_selecionado)

        lista_disponibilidade_anuncio[indice_selecionado] = 0

    tempo.exibe(1)
    return matriz_solucao


def obtem_menor_e_maior_ganhos_disponiveis(matriz_anuncio, quantidade_anuncios, lista_disponibilidade_anuncio):

    tempo = RegistroTempo('Obter limites de ganho')
    menor_ganho = None
    maior_ganho = None

    for i in range(quantidade_anuncios):
        if lista_disponibilidade_anuncio[i]:
            ganho = matriz_anuncio[i][GANHO]
            if menor_ganho is None:
                menor_ganho = ganho
                maior_ganho = ganho
            elif ganho < menor_ganho:
                menor_ganho = ganho
            elif ganho > maior_ganho:
                maior_ganho = ganho

    tempo.exibe()
    return menor_ganho, maior_ganho


def obtem_lista_indice_anuncio_candidato(matriz_anuncio, limite_inferior, quantidade_anuncios, lista_disponibilidade_anuncio):
    tempo = RegistroTempo('Obter candidatos')
    lista_indice = []
    for i in range(quantidade_anuncios):
        anuncio = matriz_anuncio[i]
        if lista_disponibilidade_anuncio[i] and anuncio[GANHO] >= limite_inferior:
            lista_indice.append(i)
    tempo.exibe(1)
    return lista_indice


def escolhe_candidato(lista_indice_anuncio_candidato):
    return lista_indice_anuncio_candidato[rd.randint(0, len(lista_indice_anuncio_candidato) - 1)]


def insere_first_fit(matriz_solucao, candidato, indice_candidato, matriz_conflito, ambiente: Ambiente):

    tempo = RegistroTempo('First Fit')
    frequencia_anuncio = candidato[FREQUENCIA]

    lista_indice_quadro_selecionado = [-1] * frequencia_anuncio
    contagem_quadros = 0

    for indice_quadro in range(ambiente.quantidade_quadros):
        if pode_ser_inserido(matriz_solucao[indice_quadro], candidato, indice_candidato, matriz_conflito, ambiente.tamanho_quadro):
            lista_indice_quadro_selecionado[contagem_quadros] = indice_quadro
            contagem_quadros = contagem_quadros + 1
        if contagem_quadros == frequencia_anuncio:
            insere_na_solucao(matriz_solucao, lista_indice_quadro_selecionado, candidato, indice_candidato)
            break

    tempo.exibe(1)


def insere_na_solucao(matriz_solucao, lista_quadro_selecionado, anuncio, indice_anuncio):

    tempo = RegistroTempo('Inserir na solução')
    tamanho_anuncio = anuncio[TAMANHO]

    for indice_quadro in lista_quadro_selecionado:
        matriz_solucao[indice_quadro][ESPACO_OCUPADO] = matriz_solucao[indice_quadro][ESPACO_OCUPADO] + tamanho_anuncio
        matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].append(indice_anuncio)

    tempo.exibe(1)


def exibe_iteracao(iteracao, matriz_anuncio, matriz_solucao, lista_disponibilidade_anuncio, limite_inferior=None, lista_candidato=None, candidato_selecionado=None):
    if EXIBE_ITERACAO:

        print(f'\nIteração {iteracao + 1}:')

        df_anuncio = DataFrame(matriz_anuncio, columns=['Tamanho', 'Frequencia', 'Ganho'])
        lista_anuncio_disponivel = [i for i, x in enumerate(lista_disponibilidade_anuncio) if x == 1]

        print('\nAnúncios disponíveis C:')
        print(df_anuncio.filter(lista_anuncio_disponivel, axis=0))

        if limite_inferior != None:
            print(f'\nLimite inferior: {limite_inferior}')

        if lista_candidato != None:
            print(f'\nCandidatos RC:')
            print(df_anuncio.filter(lista_candidato, axis=0))

        if candidato_selecionado != None:
            print('\nCandidato selecionado A_j:')
            print(df_anuncio.filter([candidato_selecionado], axis=0))

        print('\nSolução parcial S:')
        print(DataFrame(matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos']))

        print('\n==================================\n')


def solucao_vazia(quantidade_quadros):
    tempo = RegistroTempo('Construir solução vazia')
    matriz_solucao = []
    for _ in range(quantidade_quadros):
        matriz_solucao.append([0, []])
    tempo.exibe(1)
    return matriz_solucao
