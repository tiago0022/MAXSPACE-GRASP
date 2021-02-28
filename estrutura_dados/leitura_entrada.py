import csv

from modelagem.ambiente import Ambiente
from modelagem.anuncio import FREQUENCIA, TAMANHO, obtem_anuncio
from tempo_execucao import RegistroTempo

ATIVA_VALIDACAO = 0  # padrão = False
EXIBE_TEMPO = 0  # padrão = False


def obtem_ambiente(caminho):
    tempo = RegistroTempo('Ler csv ambiente')
    arquivo = open(caminho, "r")
    matriz = list(csv.reader(arquivo))
    arquivo.close()
    tempo.exibe() if EXIBE_TEMPO else None
    return Ambiente(int(matriz[1][0]), int(matriz[1][1]))


def obtem_matriz_anuncio(caminho):
    tempo = RegistroTempo('Ler csv anuncios')
    arquivo = open(caminho, "r")
    arquivo_csv = csv.reader(arquivo)
    matriz = [obtem_anuncio(linha) for linha in arquivo_csv if linha]
    arquivo.close()
    tempo.exibe() if EXIBE_TEMPO else None
    return matriz


def obtem_matriz_conflito(caminho):
    tempo = RegistroTempo('Ler csv conflitos')
    arquivo = open(caminho, "r")
    arquivo_csv = csv.reader(arquivo)
    matriz_conflito = []
    for linha in arquivo_csv:
        linha = [True if x == '1' else False for x in linha]
        matriz_conflito.append(linha)
    arquivo.close()
    tempo.exibe(1) if EXIBE_TEMPO else None
    return matriz_conflito


def obtem_instancia(caminho_instancia: str):

    ambiente = obtem_ambiente(caminho_instancia + 'ambiente.csv')
    matriz_anuncio = obtem_matriz_anuncio(caminho_instancia + 'anuncios.csv')
    # matriz_conflito = obtem_matriz_conflito(caminho_instancia + 'conflitos.csv')

    # valida_entrada(ambiente, matriz_anuncio, matriz_conflito)
    valida_entrada(ambiente, matriz_anuncio)

    return matriz_anuncio, ambiente # , matriz_conflito


# def valida_entrada(ambiente, matriz_anuncio, matriz_conflito):
def valida_entrada(ambiente, matriz_anuncio):

    if ATIVA_VALIDACAO:
        tempo = RegistroTempo('Validar entrada')

        valida_ambiente(ambiente)
        valida_anuncio(matriz_anuncio)
        # valida_conflito(matriz_conflito)

        # if len(matriz_anuncio) != len(matriz_conflito):
        #     raise Exception("Tabela de conflitos está com índices diferentes dos anúncios")

        tempo.exibe(1)


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
        if matriz_anuncio[i][TAMANHO] <= 0:
            raise Exception('Tamanho de anúncio inválido')
        if matriz_anuncio[i][FREQUENCIA] <= 0:
            raise Exception('Frequencia de anúncio inválido')


def valida_conflito(matriz_conflito):

    quantidade_anuncio = len(matriz_conflito)
    if quantidade_anuncio <= 0:
        raise Exception('Quantidade de conflitos inválida')
