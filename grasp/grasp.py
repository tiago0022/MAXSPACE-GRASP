import csv

import numpy as np
from estrutura_dados.leitura_entrada import obtem_instancia
from modelagem.solucao import Solucao
from tempo_execucao import RegistroTempo

from grasp.busca_local import BuscaLocal
from grasp.construcao import Construcao

EXIBE_INSTANCIA = 0  # padrão = False
EXIBE_TEMPO = 1  # padrão = True
EXIBE_TEMPO_DETALHE = 0  # padrão = False
EXIBE_SOLUCAO = 0  # padrão = False
EXIBE_SOLUCAO_DETALHE = 0  # padrão = False
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
    lista_tempo_construcao = None
    lista_tempo_busca_local = None

    melhor_iteracao = None
    lista_iteracao = None

    construtor = None
    buscador_local = None

    solucao: Solucao = None

    def __init__(self, caminho_instancia, quantidade_iteracoes, alpha, ignora_conflitos=False):

        self.quantidade_iteracoes = quantidade_iteracoes
        self.alpha = alpha

        self.tempo_leitura = RegistroTempo('Tempo para ler entrada')
        self.tempo_solucao = RegistroTempo('Tempo para encontrar a solução', inicializa_agora=False)
        self.tempo_exibicao = RegistroTempo('Tempo para exibir a solução', inicializa_agora=False)
        self.tempo_total = RegistroTempo('Tempo total de execução')

        self.matriz_anuncio, self.ambiente, self.matriz_conflito = obtem_instancia(caminho_instancia)

        if ignora_conflitos:
            self.esvazia_conflito()

        self.tempo_leitura.finaliza()

        self.construtor = Construcao(self.matriz_anuncio, self.matriz_conflito, self.ambiente)
        self.buscador_local = BuscaLocal(self.matriz_anuncio, self.ambiente)

        print(f'\n{caminho_instancia}')
        self.exibe_instancia()

    def esvazia_conflito(self):
        for linha in self.matriz_conflito:
            for i in range(len(linha)):
                linha[i] = False

    def limpa_solucao(self):
        self.solucao = Solucao(self.ambiente, self.matriz_conflito, self.matriz_anuncio)
        self.lista_iteracao = []

    def soluciona(self):

        self.inicializa_tempo()
        self.limpa_solucao()

        print('\n0%')
        for iteracao in range(self.quantidade_iteracoes):

            tempo_construcao = RegistroTempo()
            solucao_construida = self.construtor.constroi(self.alpha)
            self.lista_tempo_construcao.append(tempo_construcao.finaliza())

            tempo_busca_local = RegistroTempo()
            solucao_atual = self.buscador_local.busca(solucao_construida)
            self.lista_tempo_busca_local.append(tempo_busca_local.finaliza())

            if solucao_atual.espaco_total_ocupado > self.solucao.espaco_total_ocupado:
                self.solucao = solucao_atual
                self.melhor_iteracao = iteracao
                if self.solucao.eh_otimo():
                    self.registra_iteracao(iteracao, solucao_construida, solucao_atual)
                    break

            self.registra_iteracao(iteracao, solucao_construida, solucao_atual)

            if EXIBE_SOLUCAO_DETALHE:
                print(f'\n{iteracao + 1}', '- solução:')
                print(solucao_atual.metricas())

                print('===================\n')
            print(np.round(100 * (iteracao + 1) / self.quantidade_iteracoes), '%')

        self.tempo_solucao.finaliza()

        self.exibe_solucao()
        self.exibe_tempo()

        return self.solucao

    def inicializa_tempo(self):
        self.tempo_solucao.inicializa()
        self.lista_tempo_construcao = []
        self.lista_tempo_busca_local = []

    def registra_iteracao(self, iteracao, solucao_construcao: Solucao, solucao_busca_local: Solucao):
        linha_iteracao = [iteracao, solucao_construcao.espaco_total_ocupado, solucao_busca_local.espaco_total_ocupado, self.solucao.espaco_total_ocupado]
        self.lista_iteracao.append(linha_iteracao)

    def exibe_tempo(self):
        if EXIBE_TEMPO:
            print('Quantidade de anúncios:', len(self.matriz_anuncio))

            if EXIBE_TEMPO_DETALHE:
                print()
                self.buscador_local.exibe_tempo()
                RegistroTempo.exibe_soma(self.lista_tempo_construcao, 'Total Construção')
                RegistroTempo.exibe_soma(self.lista_tempo_busca_local, 'Total Busca local', nova_linha=True)

            self.tempo_leitura.exibe(ignora_inativacao=1)
            self.tempo_solucao.exibe(ignora_inativacao=1, nova_linha=(not EXIBE_SOLUCAO))

            if EXIBE_SOLUCAO:
                self.tempo_exibicao.exibe(nova_linha=1, ignora_inativacao=1)
            self.tempo_total.exibe(nova_linha=1, ignora_inativacao=1)

    def exibe_solucao(self):
        self.tempo_exibicao.inicializa()
        if EXIBE_SOLUCAO:
            print(f'\nSolução construída:\n{self.solucao}')
        if EXIBE_APROVEITAMENTO:
            print(self.solucao.avaliacao())
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

    def salva_solucao(self, local):
        arquivo = open(local, 'w+')
        arquivo_csv = csv.writer(arquivo)
        for quadro in self.solucao.matriz_solucao:
            arquivo_csv.writerow(quadro)
        arquivo.close()

    def salva_lista_iteracao(self, local):
        arquivo = open(local, 'w+')
        arquivo_csv = csv.writer(arquivo)
        for iteracao in self.lista_iteracao:
            arquivo_csv.writerow(iteracao)
        arquivo.close()
