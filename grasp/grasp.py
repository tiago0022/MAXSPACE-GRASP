import numpy as np
from estrutura_dados.leitura_entrada import obtem_instancia
from modelagem.solucao import Solucao
from tempo_execucao import RegistroTempo

from grasp.busca_local import BuscaLocal
from grasp.construcao import Construcao

EXIBE_INSTANCIA = 0  # padrão = False
EXIBE_TEMPO = 1  # padrão = True
EXIBE_SOLUCAO = 0  # padrão = False
EXIBE_APROVEITAMENTO = 1  # padrão = True


class Grasp:

    quantidade_iteracoes = None
    alpha = None

    matriz_anuncio = None
    matriz_conflito = None
    ambiente = None

    tempo_total = None
    tempo_leitura = None
    tempo_solucao = None
    tempo_exibicao = None

    construtor = None
    buscador_local = None

    solucao: Solucao = None

    def __init__(self, caminho_instancia, quantidade_iteracoes, alpha):

        self.quantidade_iteracoes = quantidade_iteracoes
        self.alpha = alpha

        self.tempo_leitura = RegistroTempo('Tempo para ler entrada')
        self.tempo_solucao = RegistroTempo('Tempo para encontrar a solução', inicializa_agora=False)
        self.tempo_exibicao = RegistroTempo('Tempo para exibir a solução', inicializa_agora=False)
        self.tempo_total = RegistroTempo('Tempo total de execução')

        self.matriz_anuncio, self.ambiente, self.matriz_conflito = obtem_instancia(caminho_instancia)
        self.tempo_leitura.finaliza()

        self.construtor = Construcao(self.matriz_anuncio, self.matriz_conflito, self.ambiente)
        self.buscador_local = BuscaLocal(self.matriz_anuncio, self.ambiente)

        self.exibe_instancia()

    def limpa_solucao(self):
        self.solucao = Solucao(self.ambiente, self.matriz_conflito, self.matriz_anuncio)

    def soluciona(self):

        self.tempo_solucao.inicializa()
        self.limpa_solucao()

        for iteracao in range(self.quantidade_iteracoes):

            solucao_construida = self.construtor.constroi(self.alpha)
            solucao_atual = self.buscador_local.busca(solucao_construida)

            if solucao_atual.espaco_total_ocupado() > self.solucao.espaco_total_ocupado():
                self.solucao = solucao_atual

            print(np.round(100 * (iteracao + 1) / self.quantidade_iteracoes, 2), '%')

        self.tempo_solucao.finaliza()

        self.exibe_solucao()
        self.exibe_tempo()

    def exibe_tempo(self):
        if EXIBE_TEMPO:
            print('Quantidade de anúncios:', len(self.matriz_anuncio))
            self.tempo_leitura.exibe(ignora_inativacao=1)
            self.tempo_solucao.exibe(ignora_inativacao=1)
            if EXIBE_SOLUCAO or EXIBE_APROVEITAMENTO:
                self.tempo_exibicao.exibe(nova_linha=1, ignora_inativacao=1)
            self.tempo_total.exibe(nova_linha=1, ignora_inativacao=1)

    def exibe_solucao(self):
        self.tempo_exibicao.inicializa()
        if EXIBE_SOLUCAO:
            print(f'\nSolução construída:\n{self.solucao}')
        if EXIBE_APROVEITAMENTO:
            print(f'\nEspaço ocupado: {round(self.solucao.proporcao_espaco_ocupado() * 100, 2)}%\n')
        self.tempo_exibicao.finaliza()

    def exibe_instancia(self):
        if EXIBE_INSTANCIA:
            print('Tamanho do quadro L:', self.ambiente.tamanho_quadro)
            print('Quantidade de quadros B:', self.ambiente.quantidade_quadros, '\n')
            print('Anúncios A_i:\n', np.array(self.matriz_anuncio), '\n')
            print('Conflitos C_ij:')
            n = len(self.matriz_conflito)
            for i in range(6 if n > 6 else n):
                print('', self.matriz_conflito[i])
            if n > 6:
                print(' ...')
            print()
