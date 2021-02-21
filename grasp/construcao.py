
import random as rd

from modelagem.ambiente import Ambiente
from modelagem.quadro import pode_ser_inserido
from pandas import DataFrame
from tempo_execucao import RegistroTempo

EXIBE_ITERACAO = 1  # Padrão = False

# Indices
TAMANHO = 0
FREQUENCIA = 1
GANHO = 2
INSERIDO = 3


def constroi(matriz_anuncio, matriz_conflito, ambiente: Ambiente, aleatoriedade, seed=1):

    matriz_solucao = solucao_vazia(ambiente.quantidade_quadros)
    contagem_anuncio_disponivel = len(matriz_anuncio)

    iteracao = 0
    while contagem_anuncio_disponivel > 0:

        menor_ganho, maior_ganho = obtem_menor_e_maior_ganhos_disponiveis(matriz_anuncio)

        limite_inferior = maior_ganho - aleatoriedade * (maior_ganho - menor_ganho)

        lista_indice_anuncio_candidato = obtem_lista_indice_anuncio_candidato(matriz_anuncio, limite_inferior)
        candidato_selecionado = escolhe_candidato(lista_indice_anuncio_candidato)

        exibe_iteracao(iteracao, matriz_anuncio, limite_inferior, lista_indice_anuncio_candidato, candidato_selecionado, matriz_solucao)

        insere_first_fit(matriz_solucao, candidato_selecionado, matriz_conflito, tamanho_quadro)
        contagem_anuncio_disponivel.drop(candidato_selecionado.index, inplace=True)
        iteracao = iteracao + 1

    return matriz_solucao


def obtem_menor_e_maior_ganhos_disponiveis(matriz_anuncio):

    tempo = RegistroTempo('Tempo para obter limites de ganho')
    menor_ganho = None
    maior_ganho = None

    for anuncio in matriz_anuncio:
        ganho = anuncio[GANHO]
        if not anuncio[INSERIDO]:
            if menor_ganho is None:
                menor_ganho = ganho
                maior_ganho = ganho
            elif ganho < menor_ganho:
                menor_ganho = ganho
            elif ganho > maior_ganho:
                maior_ganho = ganho

    tempo.exibe(0)
    return menor_ganho, maior_ganho


def obtem_lista_indice_anuncio_candidato(matriz_anuncio, limite_inferior):
    tempo = RegistroTempo('Tempo para obter candidatos')
    lista_indice = []
    for i in range(len(matriz_anuncio)):
        anuncio = matriz_anuncio[i]
        if not anuncio[INSERIDO] and anuncio[GANHO] >= limite_inferior:
            lista_indice.append(i)
    tempo.exibe()
    return lista_indice


def escolhe_candidato(lista_indice_anuncio_candidato):
    return lista_indice_anuncio_candidato[rd.randint(0, len(lista_indice_anuncio_candidato) - 1)]


def insere_first_fit(df_solucao: DataFrame, candidato: DataFrame, df_conflito, tamanho_quadro):

    frequencia_anuncio = candidato['frequencia'].values[0]

    lista_quadro_selecionado = []

    for indice_quadro, quadro in df_solucao.iterrows():
        if pode_ser_inserido(quadro, candidato, df_conflito, tamanho_quadro):
            lista_quadro_selecionado.append(indice_quadro)
        if len(lista_quadro_selecionado) == frequencia_anuncio:
            insere_na_solucao(df_solucao, lista_quadro_selecionado, candidato)
            break


def insere_na_solucao(df_solucao: DataFrame, lista_quadro_selecionado, anuncio: DataFrame):

    indice_anuncio = anuncio.first_valid_index()
    tamanho_anuncio = anuncio['tamanho'].values[0]

    for indice_quadro in lista_quadro_selecionado:
        df_solucao.at[indice_quadro, 'espaco_ocupado'] = df_solucao.at[indice_quadro, 'espaco_ocupado'] + tamanho_anuncio
        df_solucao.at[indice_quadro, 'lista_indice_anuncio'] = df_solucao.at[indice_quadro, 'lista_indice_anuncio'] + [indice_anuncio]


def exibe_iteracao(iteracao, matriz_anuncio, limite_inferior, lista_candidato, candidato_selecionado, matriz_solucao):
    if EXIBE_ITERACAO:
        df_anuncio = DataFrame(matriz_anuncio, columns=['Tamanho', 'Frequencia', 'Ganho', 'Inserido'])
        print(f'Iteração {iteracao + 1}:\n\nAnúncios disponíveis C:')
        print(df_anuncio)
        print(f'\nLimite inferior: {limite_inferior}\n\nCandidatos RC:')
        print(df_anuncio.filter(lista_candidato, axis=0))
        print('\nCandidato selecionado A_j:')
        print(df_anuncio.filter([candidato_selecionado], axis=0))
        print('\nSolução parcial S:')
        print(DataFrame(matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos']))
        print('\n==================================\n')


def solucao_vazia(quantidade_quadros):
    return [[0, []]] * quantidade_quadros
