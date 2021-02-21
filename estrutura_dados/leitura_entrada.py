import csv

from modelagem.ambiente import Ambiente
from tempo_execucao import RegistroTempo

ATIVA_VALIDACAO = 0  # padrão = False


def obtem_ambiente(caminho):
    arquivo = open(caminho, "r")
    matriz = list(csv.reader(arquivo))
    arquivo.close()
    return Ambiente(int(matriz[1][0]), int(matriz[1][1]))


def obtem_matriz_anuncio(caminho):
    arquivo = open(caminho, "r")
    arquivo_csv = csv.reader(arquivo)
    matriz = [[int(linha[0]), int(linha[1])] for linha in arquivo_csv if linha]
    arquivo.close()
    return matriz


def obtem_matriz_conflito(caminho):
    arquivo = open(caminho, "r")
    arquivo_csv = csv.reader(arquivo)
    matriz_conflito = []
    for linha in arquivo_csv:
        linha = list(map(bool, linha))
        matriz_conflito.append(linha)
    arquivo.close()
    return matriz_conflito


def obtem_instancia(caminho_instancia: str):

    tempo = RegistroTempo('Tempo para ler csv ambiente')
    ambiente = obtem_ambiente(caminho_instancia + 'ambiente.csv')
    tempo.exibe()

    tempo = RegistroTempo('Tempo para ler csv anuncios')
    matriz_anuncio = obtem_matriz_anuncio(caminho_instancia + 'anuncios.csv')
    tempo.exibe()

    tempo = RegistroTempo('Tempo para ler csv conflitos')
    matriz_conflito = obtem_matriz_conflito(caminho_instancia + 'conflitos.csv')
    tempo.exibe(1)

    tempo = RegistroTempo('Tempo para validação da entrada')
    valida_entrada(ambiente, matriz_anuncio, matriz_conflito)
    tempo.exibe(1)

    return matriz_anuncio, matriz_conflito, ambiente


def valida_entrada(ambiente, matriz_anuncio, matriz_conflito):

    if ATIVA_VALIDACAO:

        valida_ambiente(ambiente)
        valida_anuncio(matriz_anuncio)
        valida_conflito(matriz_conflito)

        if len(matriz_anuncio) != len(matriz_conflito):
            raise Exception("Tabela de conflitos está com índices diferentes dos anúncios")


def valida_ambiente(ambiente: Ambiente):

    if ambiente.tamanho_quadro <= 0:
        raise Exception('Tamanho de quadro inválido')

    if ambiente.quantidade_quadros <= 0:
        raise Exception('Quantidade de quadros inválida')


def valida_anuncio(matriz_anuncio):

    quantidade_anuncios = len(matriz_anuncio)

    if quantidade_anuncios <= 0:
        raise Exception('Quantidade de anúncios inválida')

    for i in range(quantidade_anuncios):
        if matriz_anuncio[i][0] <= 0:
            raise Exception('Tamanho de anúncio inválido')
        if matriz_anuncio[i][1] <= 0:
            raise Exception('Frequencia de anúncio inválido')


def valida_conflito(matriz_conflito):

    quantidade_anuncio = len(matriz_conflito)
    if quantidade_anuncio <= 0:
        raise Exception('Quantidade de conflitos inválida')

    for i in range(quantidade_anuncio):
        for j in range(i):
            elemento = matriz_conflito[i][j]
            if elemento != 1 and elemento != 0:
                raise Exception('Tabela de conflitos possui valor inválido')
