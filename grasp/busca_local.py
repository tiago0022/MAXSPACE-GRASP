from modelagem.ambiente import Ambiente
from modelagem.anuncio import TAMANHO
from modelagem.solucao import Solucao
from tempo_execucao import RegistroTempo

EXIBE_TEMPO = 0  # padrão = False


class BuscaLocal:

    _matriz_anuncio = None
    _ambiente: Ambiente = None

    _lista_tempo_adiciona = None
    _lista_tempo_substitui = None
    _lista_tempo_move = None
    _lista_tempo_remaneja = None

    def __init__(self, matriz_anuncio, ambiente):
        self._matriz_anuncio = matriz_anuncio
        self._ambiente = ambiente
        self._inicializa_tempo()

    def busca(self, solucao_inicial: Solucao) -> Solucao:

        melhor_solucao = solucao_inicial
        iteracao = 1

        while True:

            # print(f'\n{iteracao} - solução:')
            # print(melhor_solucao.metricas())

            vizinho = self._obtem_melhor_vizinho(melhor_solucao)

            if vizinho != None:
                melhor_solucao = vizinho
                if melhor_solucao.eh_otimo():
                    return melhor_solucao
            else:
                return melhor_solucao

            iteracao += 1

    def _inicializa_tempo(self):
        self._lista_tempo_adiciona = []
        self._lista_tempo_substitui = []
        self._lista_tempo_move = []
        self._lista_tempo_remaneja = []

    def exibe_tempo(self):
        if EXIBE_TEMPO:

            print('Entrei em cada vizinhança:')
            print('Adiciona:', len(self._lista_tempo_adiciona), 'vezes')
            print('Substitui:', len(self._lista_tempo_substitui), 'vezes')
            print('Move:', len(self._lista_tempo_move), 'vezes')
            print('Remaneja:', len(self._lista_tempo_remaneja), 'vezes\n')

            RegistroTempo.exibe_soma(self._lista_tempo_adiciona, 'Total adiciona')
            RegistroTempo.exibe_soma(self._lista_tempo_substitui, 'Total substitui')
            RegistroTempo.exibe_soma(self._lista_tempo_move, 'Total move')
            RegistroTempo.exibe_soma(self._lista_tempo_remaneja, 'Total remaneja', nova_linha=True)

    def _obtem_melhor_vizinho(self, solucao: Solucao) -> Solucao:

        tempo = RegistroTempo()
        solucao_adiciona = self._melhor_vizinho_adiciona(solucao)
        self._lista_tempo_adiciona.append(tempo.finaliza())
        if solucao_adiciona != None:
            # print('Adicionou\n')
            return solucao_adiciona
        # print('Não adicionou\n')

        tempo = RegistroTempo()
        solucao_substitui = self._melhor_vizinho_substitui(solucao)
        self._lista_tempo_substitui.append(tempo.finaliza())
        if solucao_substitui != None:
            # print('Substituiu\n')
            return solucao_substitui
        # print('Não substituiu\n')

        tempo = RegistroTempo()
        solucao_move = self._melhor_vizinho_move(solucao)
        self._lista_tempo_move.append(tempo.finaliza())
        if solucao_move != None:
            # print('Moveu\n')
            return solucao_move
        # print('Não moveu\n')

        tempo = RegistroTempo()
        solucao_remaneja = self._melhor_vizinho_remaneja(solucao)
        self._lista_tempo_remaneja.append(tempo.finaliza())
        if solucao_remaneja != None:
            # print('Remanejou\n')
            return solucao_remaneja
        # print('Não remanejou\n')

        return None

    def _melhor_vizinho_adiciona(self, solucao: Solucao) -> Solucao:
        melhor = solucao
        melhor_encontrado = False
        for i in solucao.lista_anuncio_disponivel:
            solucao_adiciona = solucao.adiciona(i)
            if solucao_adiciona != None and solucao_adiciona.eh_melhor(melhor):
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
                if solucao_substitui != None and solucao_substitui.eh_melhor(melhor):
                    # print(i, 'removido e', j, 'adicionado')
                    melhor = solucao_substitui
                    melhor_encontrado = True
        return melhor if melhor_encontrado else None

    def _melhor_vizinho_move(self, solucao: Solucao) -> Solucao:
        melhor = solucao
        melhor_encontrado = False
        for i in solucao.lista_anuncio_adicionado:
            for quadro_i in solucao.matriz_anuncio_quadro[i]:
                espaco_livre_suficiente_k = self._matriz_anuncio[i][TAMANHO]
                while espaco_livre_suficiente_k <= self._ambiente.tamanho_quadro:
                    for quadro_k in solucao.dicionario_espaco_quadro[espaco_livre_suficiente_k]:
                        solucao_move = solucao.move(i, quadro_i, quadro_k)
                        if solucao_move != None and solucao_move.eh_melhor(melhor):
                            # print(i, 'no quadro', quadro_i, 'movido para o quadro', quadro_k)
                            melhor = solucao_move
                            melhor_encontrado = True
                    espaco_livre_suficiente_k += 1
        return melhor if melhor_encontrado else None

    def _melhor_vizinho_remaneja(self, solucao: Solucao) -> Solucao:
        melhor = solucao
        melhor_encontrado = False
        for i in solucao.lista_anuncio_adicionado:
            for quadro_i in solucao.matriz_anuncio_quadro[i]:
                for j in solucao.lista_anuncio_adicionado:
                    for quadro_j in solucao.matriz_anuncio_quadro[j]:
                        solucao_remaneja = solucao.remaneja(i, quadro_i, j, quadro_j)
                        if solucao_remaneja != None and solucao_remaneja.eh_melhor(melhor):
                            # print(i, 'no quadro', quadro_i, 'trocado com', j, 'do quadro', quadro_j)
                            melhor = solucao_remaneja
                            melhor_encontrado = True
        return melhor if melhor_encontrado else None
