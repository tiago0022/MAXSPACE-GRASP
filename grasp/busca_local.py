from modelagem.solucao import Solucao

# Classe incompleta


class BuscaLocal:

    ambiente = None

    def __init__(self, ambiente):
        self.ambiente = ambiente

    def busca(self, solucao_inicial: Solucao) -> Solucao:

        melhor_solucao = solucao_inicial

        while True:

            vizinho = self._obtem_melhor_vizinho(melhor_solucao)

            if vizinho.ehMelhor(melhor_solucao):
                melhor_solucao = vizinho
            else:
                return melhor_solucao

    def _obtem_melhor_vizinho(self, solucao: Solucao) -> Solucao:

        melhor_vizinho = Solucao(self.ambiente)

        # for anuncio_i in matriz_anuncio:

        #     solucao_adiciona = solucao.adiciona(anuncio_i)
        #     if solucao_adiciona.ehMelhor(melhor_vizinho):
        #         melhor_vizinho = solucao_adiciona

        #     for anuncio_j in matriz_anuncio:

        #         solucao_troca = solucao.troca(anuncio_i, anuncio_j)
        #         if solucao_troca.ehMelhor(melhor_vizinho):
        #             melhor_vizinho = solucao_troca

        #         solucao_remaneja = solucao.remaneja(anuncio_i, anuncio_j)
        #         if solucao_remaneja.ehMelhor(melhor_vizinho):
        #             melhor_vizinho = solucao_remaneja

        #     for quadro in lista_quadro_disponiveis:

        #         solucao_move = solucao.move(anuncio_i, quadro)
        #         if solucao_move.ehMelhor(melhor_vizinho):
        #             melhor_vizinho = solucao_move

        return melhor_vizinho
