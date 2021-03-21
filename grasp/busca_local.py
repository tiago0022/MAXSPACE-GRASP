from modelagem.solucao import espaco_total_ocupado


class BuscaLocal:

    def __init__(self):
        pass

    def busca(self, matriz_solucao_inicial):

        melhor_solucao = matriz_solucao_inicial
        melhor_espaco_ocupado = 0

        solucao_atual = matriz_solucao_inicial
        avaliacao_atual = 0

        while True:

            vizinho, avaliacao_vizinho, espaco_ocupado_vizinho = self.obtem_melhor_vizinho(solucao_atual)

            if avaliacao_vizinho >= avaliacao_atual:
                avaliacao_atual = avaliacao_vizinho
                solucao_atual = vizinho
            else:
                return melhor_solucao

            if espaco_ocupado_vizinho > melhor_espaco_ocupado:
                melhor_espaco_ocupado = espaco_ocupado_vizinho
                melhor_solucao = vizinho

    def metrica_para_avaliar_solucao(self, solucao):

        # L = tamanho_quadro
        # B = quantidade_quadros
        # beta = 0.9  # parâmetro configurável

        # EO = beta * (solucao.espaco_ocupado / (L * B))  # Termo que representa o espaço ocupado
        # QQC = (1 - beta) * (solucao.quantidade_quadros_completos / B)  # Termo que representa a quantidade de quados completos

        # return EO + QQC
