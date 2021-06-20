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

            # print(f'\n{iteracao} - solução:')
            # print(melhor_solucao.metricas())

            vizinho = self._obtem_melhor_vizinho(melhor_solucao)

            if vizinho != None:
                melhor_solucao = vizinho
            else:
                return melhor_solucao

            iteracao += 1

    def _obtem_melhor_vizinho(self, solucao: Solucao) -> Solucao:

        solucao_adiciona = self._melhor_vizinho_adiciona(solucao)
        if solucao_adiciona != None:
            return solucao_adiciona

        solucao_substitui = self._melhor_vizinho_substitui(solucao)
        if solucao_substitui != None:
            return solucao_substitui

        solucao_move = self._melhor_vizinho_move(solucao)
        if solucao_move != None:
            return solucao_move

        solucao_remaneja = self._melhor_vizinho_remaneja(solucao)
        if solucao_remaneja != None:
            return solucao_remaneja

        return None

    def _melhor_vizinho_adiciona(self, solucao: Solucao) -> Solucao:
        melhor = solucao
        melhor_encontrado = False
        for i in solucao.lista_anuncio_disponivel:
            solucao_adiciona = solucao.adiciona(i)
            if solucao_adiciona != None and solucao_adiciona.ehMelhor(melhor):
                # print(i, 'adicionado')
                melhor = solucao_adiciona
                melhor_encontrado = True
        return melhor if melhor_encontrado else None

    def _melhor_vizinho_substitui(self, solucao: Solucao) -> Solucao:
        melhor = solucao
        melhor_encontrado = False
        for i in solucao.lista_anuncio_adicionado:
            for j in solucao.lista_anuncio_disponivel:
                solucao_substitui = solucao.substitui(i, j)
                if solucao_substitui != None and solucao_substitui.ehMelhor(melhor):
                    # print(i, 'removido e', j, 'adicionado')
                    melhor = solucao_substitui
                    melhor_encontrado = True
        return melhor if melhor_encontrado else None

    def _melhor_vizinho_move(self, solucao: Solucao) -> Solucao:
        melhor = solucao
        melhor_encontrado = False
        for i in solucao.lista_anuncio_adicionado:
            for quadro_i in solucao.matriz_anuncio_quadro[i]:
                for quadro_k in solucao.lista_quadro_disponivel:
                    solucao_move = solucao.move(i, quadro_i, quadro_k)
                    if solucao_move != None and solucao_move.ehMelhor(melhor):
                        # print(i, 'no quadro', quadro_i, 'movido para o quadro', quadro_k)
                        melhor = solucao_move
                        melhor_encontrado = True
                        return melhor
        return melhor if melhor_encontrado else None

    def _melhor_vizinho_remaneja(self, solucao: Solucao) -> Solucao:
        melhor = solucao
        melhor_encontrado = False
        for i in solucao.lista_anuncio_adicionado:
            for quadro_i in solucao.matriz_anuncio_quadro[i]:
                for j in solucao.lista_anuncio_adicionado:
                    for quadro_j in solucao.matriz_anuncio_quadro[j]:
                        solucao_remaneja = solucao.remaneja(i, quadro_i, j, quadro_j)
                        if solucao_remaneja != None and solucao_remaneja.ehMelhor(melhor):
                            # print(i, 'no quadro', quadro_i, 'trocado com', j, 'do quadro', quadro_j)
                            melhor = solucao_remaneja
                            melhor_encontrado = True
                            return melhor
        return melhor if melhor_encontrado else None
