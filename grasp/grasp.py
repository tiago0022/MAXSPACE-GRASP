from numpy.core.numeric import False_
from estrutura_dados.leitura_entrada import obtem_instancia
from tempo_execucao import RegistroTempo

from grasp.construcao import constroi

EXIBE_INSTANCIA = 0
EXIBE_TEMPO = 1
EXIBE_SOLUCAO = 0


class Grasp:

    alpha = None
    seed = None
    df_anuncio = None
    df_conflito = None
    tamanho_quadro = None
    quantidade_quadros = None

    tempo_total = None
    tempo_leitura = None
    tempo_solucao = None

    df_solucao_construida = None

    def __init__(self, caminho_instancia, alpha, seed=1):

        self.alpha = alpha
        self.seed = seed

        self.tempo_total = RegistroTempo('Tempo total de execução')
        self.tempo_leitura = RegistroTempo('Tempo para ler entrada')
        self.tempo_solucao = RegistroTempo('Tempo para encontrar a solução', inicializa_agora=False)

        self.df_anuncio, self.df_conflito, self.tamanho_quadro, self.quantidade_quadros = obtem_instancia(caminho_instancia)
        self.tempo_leitura.finaliza()

        self.exibe_instancia()

    def soluciona(self):

        self.tempo_solucao.inicializa()
        self.df_solucao_construida = constroi(self.df_anuncio, self.df_conflito, self.tamanho_quadro, self.quantidade_quadros, self.alpha, self.seed)
        self.tempo_solucao.finaliza()

        self.exibe_solucao()
        self.exibe_tempo()

    def exibe_tempo(self):
        if EXIBE_TEMPO:
            self.tempo_leitura.exibe()
            self.tempo_solucao.exibe()
            self.tempo_total.exibe()

    def exibe_solucao(self):
        if EXIBE_SOLUCAO:
            porcentagem_espaco_ocupado = (self.df_solucao_construida['espaco_ocupado'].sum() / (self.tamanho_quadro * self.quantidade_quadros)) * 100
            print(f'Solução construída:\n{self.df_solucao_construida}\n\nEspaço ocupado: {round(porcentagem_espaco_ocupado,2)}%\n')

    def exibe_instancia(self):
        if EXIBE_INSTANCIA:
            print('Tamanho do quadro L:', self.tamanho_quadro)
            print('Quantidade de quadros B:', self.quantidade_quadros, '\n')
            print('Anúncios A_i:\n', self.df_anuncio, '\n')
            print('Conflitos C_ij:\n', self.df_conflito, '\n')
