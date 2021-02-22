import numpy as np
from pandas.core.frame import DataFrame
from estrutura_dados.leitura_entrada import obtem_instancia
from tempo_execucao import RegistroTempo

from grasp.construcao import constroi

EXIBE_INSTANCIA = 0  # padrão = False
EXIBE_TEMPO = 1  # padrão = True
EXIBE_SOLUCAO = 1  # padrão = True


class Grasp:

    alpha = None
    seed = None
    matriz_anuncio = None
    matriz_conflito = None
    ambiente = None

    tempo_total = None
    tempo_leitura = None
    tempo_solucao = None
    tempo_exibicao = None

    matriz_solucao_construida = None

    def __init__(self, caminho_instancia, alpha, seed=1):

        self.alpha = alpha
        self.seed = seed

        self.tempo_leitura = RegistroTempo('Tempo para ler entrada')
        self.tempo_solucao = RegistroTempo('Tempo para encontrar a solução', inicializa_agora=False)
        self.tempo_exibicao = RegistroTempo('Tempo para exibir a solução', inicializa_agora=False)
        self.tempo_total = RegistroTempo('Tempo total de execução')

        self.matriz_anuncio, self.matriz_conflito, self.ambiente = obtem_instancia(caminho_instancia)
        self.tempo_leitura.finaliza()

        self.exibe_instancia()

    def soluciona(self):

        self.tempo_solucao.inicializa()
        self.matriz_solucao_construida = constroi(self.matriz_anuncio, self.matriz_conflito, self.ambiente, self.alpha, self.seed)
        self.tempo_solucao.finaliza()

        self.exibe_solucao()
        self.exibe_tempo()

    def exibe_tempo(self):
        if EXIBE_TEMPO:
            self.tempo_leitura.exibe(ignora_inativacao=1)
            self.tempo_solucao.exibe(ignora_inativacao=1)
            self.tempo_exibicao.exibe(nova_linha=1, ignora_inativacao=1)
            self.tempo_total.exibe(nova_linha=1, ignora_inativacao=1)

    def exibe_solucao(self):
        self.tempo_exibicao.inicializa()
        if EXIBE_SOLUCAO:
            df_solucao = DataFrame(self.matriz_solucao_construida, columns=['Espaço ocupado', 'Anúncios inseridos'])
            espaco_ocupado = df_solucao['Espaço ocupado'].sum()
            espaco_disponivel = (self.ambiente.tamanho_quadro * self.ambiente.quantidade_quadros)
            porcentagem_espaco_ocupado = (espaco_ocupado / espaco_disponivel) * 100
            print(f'\nSolução construída:\n{df_solucao}')
            print(f'\nEspaço ocupado: {round(porcentagem_espaco_ocupado,2)}%\n')

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
