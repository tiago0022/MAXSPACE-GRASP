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

        for i, anuncio_i in enumerate(self._matriz_anuncio):

            lista_quadro_i = []

            solucao_adiciona = solucao.adiciona_ff(i)
            if solucao_adiciona is not None and solucao_adiciona.ehMelhor(melhor_vizinho):
                print(i, 'adicionado')
                melhor_vizinho = solucao_adiciona

            for j, anuncio_j in enumerate(self._matriz_anuncio):

                lista_quadro_j = []

                solucao_troca = solucao.substitui(i, j)
                if solucao_troca is not None and solucao_troca.ehMelhor(melhor_vizinho):
                    print(i, 'removido e', j, 'adicionado')
                    melhor_vizinho = solucao_troca

                for quadro_l in self._ambiente.lista_quadro():

                    if solucao.anuncio_no_quadro(i, quadro_l):
                        lista_quadro_i.append(quadro_l)
                    if solucao.anuncio_no_quadro(j, quadro_l):
                        lista_quadro_j.append(quadro_l)

                for quadro_i in lista_quadro_i:
                    for quadro_j in lista_quadro_j:
                        solucao_remaneja = solucao.remaneja(i, quadro_i, j, quadro_j)
                        if solucao_remaneja is not None and solucao_remaneja.ehMelhor(melhor_vizinho):
                            print(i, 'no quadro', quadro_i, 'trocado com', j, 'do quadro', quadro_j)
                            melhor_vizinho = solucao_remaneja

                    for quadro_l in solucao.lista_quadro_disponivel:
                        solucao_move = solucao.move(i, quadro_i, quadro_l)
                        if solucao_move is not None and solucao_move.ehMelhor(melhor_vizinho):
                            print(i, 'no quadro', quadro_i, 'movido para o quadro', quadro_l)
                            melhor_vizinho = solucao_move

        return melhor_vizinho
