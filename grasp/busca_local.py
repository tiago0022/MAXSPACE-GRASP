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

            print(iteracao, '- solução encontrada:')
            print('Espaço ocupado:', melhor_solucao.proporcao_espaco_ocupado())
            print('Critério de desempate:', melhor_solucao.criterio_desempate())
            print()

            vizinho = self._obtem_melhor_vizinho(melhor_solucao)

            if vizinho.ehMelhor(melhor_solucao):
                melhor_solucao = vizinho
            else:
                return melhor_solucao

    def _obtem_melhor_vizinho(self, solucao: Solucao) -> Solucao:

        melhor_vizinho = solucao.copia()

        for disponivel in solucao.lista_anuncio_disponivel:

            solucao_adiciona = solucao.adiciona(disponivel)
            if solucao_adiciona is not None:
                print(disponivel, 'adicionado')
                return solucao_adiciona

            for adicionado in solucao.lista_anuncio_adicionado:
                solucao_substitui = solucao.substitui(adicionado, disponivel)
                if solucao_substitui is not None and solucao_substitui.ehMelhor(solucao):
                    print(adicionado, 'removido e', disponivel, 'adicionado')
                    return solucao_substitui

        for i in solucao.lista_anuncio_adicionado:
            for j in solucao.lista_anuncio_adicionado:
                for quadro_i in solucao.matriz_anuncio_quadro[i]:
                    for quadro_j in solucao.matriz_anuncio_quadro[j]:
                        solucao_remaneja = solucao.remaneja(i, quadro_i, j, quadro_j)
                        if solucao_remaneja is not None and solucao_remaneja.ehMelhor(solucao):
                            print(i, 'no quadro', quadro_i, 'trocado com', j, 'do quadro', quadro_j)
                            return solucao_remaneja

        # for i, _ in enumerate(self._matriz_anuncio):

        #     lista_quadro_i = []

        #     for j, anuncio_j in enumerate(self._matriz_anuncio):

        #         lista_quadro_j = []

        #         for quadro_l in self._ambiente.lista_quadro():

        #             if solucao.anuncio_no_quadro(i, quadro_l):
        #                 lista_quadro_i.append(quadro_l)
        #             if solucao.anuncio_no_quadro(j, quadro_l):
        #                 lista_quadro_j.append(quadro_l)

        #             for quadro_l in solucao.lista_quadro_disponivel:
        #                 solucao_move = solucao.move(i, quadro_i, quadro_l)
        #                 if solucao_move is not None and solucao_move.ehMelhor(melhor_vizinho):
        #                     print(i, 'no quadro', quadro_i, 'movido para o quadro', quadro_l)
        #                     melhor_vizinho = solucao_move

        return melhor_vizinho
