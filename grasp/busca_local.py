from modelagem.ambiente import Ambiente
from modelagem.solucao import Solucao


class BuscaLocal:

    _matriz_anuncio = None
    _ambiente: Ambiente = None

    def __init__(self, matriz_anuncio, ambiente):
        self._matriz_anuncio = matriz_anuncio
        self._ambiente = ambiente

    def busca(self, solucao_inicial: Solucao) -> Solucao:

        melhor_solucao = solucao_inicial
        iteracao = 1

        while True:

            print(iteracao, '- solução:')
            print(melhor_solucao.metricas())

            vizinho = self._obtem_melhor_vizinho(melhor_solucao)

            if vizinho != None:
                melhor_solucao = vizinho
            else:
                return melhor_solucao

    def _obtem_melhor_vizinho(self, solucao: Solucao) -> Solucao:

        for disponivel in solucao.lista_anuncio_disponivel:

            solucao_adiciona = solucao.adiciona(disponivel)
            if solucao_adiciona != None:
                print(disponivel, 'adicionado')
                return solucao_adiciona

            for adicionado in solucao.lista_anuncio_adicionado:
                solucao_substitui = solucao.substitui(adicionado, disponivel)
                if solucao_substitui != None and solucao_substitui.ehMelhor(solucao):
                    print(adicionado, 'removido e', disponivel, 'adicionado')
                    return solucao_substitui

        for i in solucao.lista_anuncio_adicionado:
            for quadro_i in solucao.matriz_anuncio_quadro[i]:

                for quadro_k in solucao.lista_quadro_disponivel:
                    solucao_move = solucao.move(i, quadro_i, quadro_k)
                    if solucao_move != None and solucao_move.ehMelhor(solucao):
                        print(i, 'no quadro', quadro_i, 'movido para o quadro', quadro_k)
                        return solucao_move

                for j in solucao.lista_anuncio_adicionado:
                    for quadro_j in solucao.matriz_anuncio_quadro[j]:
                        solucao_remaneja = solucao.remaneja(i, quadro_i, j, quadro_j)
                        if solucao_remaneja != None and solucao_remaneja.ehMelhor(solucao):
                            print(i, 'no quadro', quadro_i, 'trocado com', j, 'do quadro', quadro_j)
                            return solucao_remaneja

        return None
