from modelagem.ambiente import Ambiente


def espaco_total_ocupado(matriz_solucao):
    espaco_ocupado = 0
    for quadro in matriz_solucao:
        espaco_ocupado += quadro[0]
    return espaco_ocupado


def proporcao_espaco_ocupado(matriz_solucao, ambiente: Ambiente):
    return espaco_total_ocupado(matriz_solucao) / ambiente.espaco_total
