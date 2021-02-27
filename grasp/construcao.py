
import random as rd

import numpy as np
from modelagem.ambiente import Ambiente
from modelagem.anuncio import FREQUENCIA, GANHO, TAMANHO
from modelagem.quadro import (ESPACO_OCUPADO, LISTA_INDICE_ANUNCIO,
                              pode_ser_inserido)
from pandas import DataFrame
from tempo_execucao import RegistroTempo

EXIBE_ITERACAO = 0  # Padrão = False
EXIBE_TEMPO = 0  # Padrão = False


class Construcao:

    def __init__(self, matriz_anuncio, matriz_conflito, ambiente):

        self.matriz_anuncio = matriz_anuncio
        self.matriz_conflito = matriz_conflito
        self.ambiente: Ambiente = ambiente

        self.matriz_solucao = None

        self.quantidade_anuncios = len(matriz_anuncio)

        self._lista_disponibilidade_anuncio = None

        self._tempo_construcao = None
        self._lista_tempo_total = None
        self._lista_tempo_limites = None
        self._lista_tempo_candidato = None
        self._lista_tempo_first_fit = None

        self._limite_inferior_atual = None
        self._menor_ganho_atual = None
        self._maior_ganho_atual = None
        self._lista_indice_anuncio_candidato_atual = None
        self._tamanho_lista_indice_anuncio_candidato_atual = None

    def _limpa_construcao(self):
        self._tempo_construcao = RegistroTempo('Construção')
        tempo = RegistroTempo('Limpar solução anterior')
        self.matriz_solucao = self._solucao_vazia()
        self._lista_disponibilidade_anuncio = [1] * self.quantidade_anuncios
        self._limpa_lista_tempo()
        self._limpa_dados_atuais()
        # tempo.exibe(1)

    def _limpa_dados_atuais(self):
        self._limite_inferior_atual = None
        self._menor_ganho_atual = None
        self._maior_ganho_atual = None
        self._lista_indice_anuncio_candidato_atual = None
        self._tamanho_lista_indice_anuncio_candidato_atual = None

    def _limpa_lista_tempo(self):
        self._lista_tempo_total = [0] * self.quantidade_anuncios
        self._lista_tempo_limites = [0] * self.quantidade_anuncios
        self._lista_tempo_candidato = [0] * self.quantidade_anuncios
        self._lista_tempo_first_fit = [0] * self.quantidade_anuncios

    def constroi(self, aleatoriedade):

        self._limpa_construcao()

        self._exibe_iteracao()

        for iteracao in range(self.quantidade_anuncios):

            tempo_iteracao = RegistroTempo()

            self._atualiza_limite_inferior_atual(aleatoriedade, iteracao)

            indice_selecionado = self._obtem_candidato(iteracao)

            self._insere_first_fit(indice_selecionado, iteracao)

            self._exibe_iteracao(iteracao, indice_selecionado)

            self._lista_disponibilidade_anuncio[indice_selecionado] = 0

            self._lista_tempo_total[iteracao] = tempo_iteracao.finaliza()

        self._exibe_dados_tempo()

        return self.matriz_solucao

    def _obtem_candidato(self, iteracao):

        tempo_candidatos = RegistroTempo()

        if self._lista_indice_anuncio_candidato_atual == None:
            self._atualiza_lista_indice_anuncio_candidato()

        indice_selecionado = self._escolhe_candidato()

        self._lista_tempo_candidato[iteracao] = tempo_candidatos.finaliza()

        return indice_selecionado

    def _atualiza_limite_inferior_atual(self, aleatoriedade, iteracao):

        tempo_limites = RegistroTempo()

        if self._maior_ganho_atual == None or self._menor_ganho_atual == None or self._limite_inferior_atual == None:

            self._atualiza_menor_e_maior_ganhos_disponiveis_atuais()

            self._limite_inferior_atual = self._maior_ganho_atual - aleatoriedade * (self._maior_ganho_atual - self._menor_ganho_atual)

            self._lista_indice_anuncio_candidato_atual = None

        self._lista_tempo_limites[iteracao] = tempo_limites.finaliza()

    def _exibe_dados_tempo(self):
        if EXIBE_TEMPO:
            print(f'\nQuantidade de iterações: {self.quantidade_anuncios}\n')

            print(f'Média por iteração: {round(np.average(self._lista_tempo_total) * 100, 1)} ms')
            print(f'Iteração mais rápida: {round(np.min(self._lista_tempo_total) * 100, 1)} ms')
            print(f'Iteração mais lenta: {round(np.max(self._lista_tempo_total) * 100, 1)} ms\n')

            print(f'Tempo total limites: {round(np.sum(self._lista_tempo_limites), 2)} s')
            print(f'Tempo total candidatos: {round(np.sum(self._lista_tempo_candidato), 2)} s')
            print(f'Tempo total first fit: {round(np.sum(self._lista_tempo_first_fit), 2)} s\n')

            self._tempo_construcao.exibe(1)

    def _atualiza_menor_e_maior_ganhos_disponiveis_atuais(self):

        tempo = RegistroTempo('Obter limites de ganho')
        menor_ganho = None
        maior_ganho = None

        for i in range(self.quantidade_anuncios):
            if self._lista_disponibilidade_anuncio[i]:
                ganho = self.matriz_anuncio[i][GANHO]
                if menor_ganho is None:
                    menor_ganho = ganho
                    maior_ganho = ganho
                elif ganho < menor_ganho:
                    menor_ganho = ganho
                elif ganho > maior_ganho:
                    maior_ganho = ganho

        self._menor_ganho_atual = menor_ganho
        self._maior_ganho_atual = maior_ganho
        # tempo.exibe()

    def _atualiza_lista_indice_anuncio_candidato(self):
        tempo = RegistroTempo('Obter candidatos')
        lista_indice = []
        tamanho_lista = 0
        for i in range(self.quantidade_anuncios):
            anuncio = self.matriz_anuncio[i]
            if self._lista_disponibilidade_anuncio[i] and anuncio[GANHO] >= self._limite_inferior_atual:
                lista_indice.append(i)
                tamanho_lista = tamanho_lista + 1
        self._lista_indice_anuncio_candidato_atual = lista_indice
        self._tamanho_lista_indice_anuncio_candidato_atual = tamanho_lista
        # tempo.exibe(1)

    def _escolhe_candidato(self):

        indice_sorteado = rd.randint(0, self._tamanho_lista_indice_anuncio_candidato_atual - 1)
        indice_candidato = self._lista_indice_anuncio_candidato_atual.pop(indice_sorteado)

        tamanho_candidato = self.matriz_anuncio[indice_candidato][GANHO]

        if tamanho_candidato == self._maior_ganho_atual:
            self._maior_ganho_atual = None

        if tamanho_candidato == self._menor_ganho_atual:
            self._menor_ganho_atual = None

        self._tamanho_lista_indice_anuncio_candidato_atual = self._tamanho_lista_indice_anuncio_candidato_atual - 1

        return indice_candidato

    def _insere_first_fit(self, indice_candidato, iteracao):

        tempo = RegistroTempo('First Fit')
        candidato = self.matriz_anuncio[indice_candidato]
        frequencia_anuncio = candidato[FREQUENCIA]

        lista_indice_quadro_selecionado = [-1] * frequencia_anuncio
        contagem_quadros = 0

        for indice_quadro in range(self.ambiente.quantidade_quadros):
            if pode_ser_inserido(self.matriz_solucao[indice_quadro], candidato, indice_candidato, self.matriz_conflito, self.ambiente.tamanho_quadro):
                lista_indice_quadro_selecionado[contagem_quadros] = indice_quadro
                contagem_quadros = contagem_quadros + 1
            if contagem_quadros == frequencia_anuncio:
                self._insere_na_solucao(lista_indice_quadro_selecionado, candidato, indice_candidato)
                break

        self._lista_tempo_first_fit[iteracao] = tempo.finaliza()
        # tempo.exibe(1)

    def _insere_na_solucao(self, lista_quadro_selecionado, anuncio, indice_anuncio):

        tempo = RegistroTempo('Inserir na solução')
        tamanho_anuncio = anuncio[TAMANHO]

        for indice_quadro in lista_quadro_selecionado:
            self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] + tamanho_anuncio
            self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].append(indice_anuncio)

        # tempo.exibe(1)

    def _exibe_iteracao(self, iteracao=None, candidato_selecionado=None):
        if EXIBE_ITERACAO:

            if iteracao != None:
                print(f'\nIteração {iteracao + 1}:')

            df_anuncio = DataFrame(self.matriz_anuncio, columns=['Tamanho', 'Frequencia', 'Ganho'])
            lista_anuncio_disponivel = [i for i, x in enumerate(self._lista_disponibilidade_anuncio) if x == 1]

            print('\nAnúncios disponíveis C:')
            print(df_anuncio.filter(lista_anuncio_disponivel, axis=0))

            if self._limite_inferior_atual != None:
                print(f'\nLimite inferior: {self._limite_inferior_atual}')

            if self._lista_indice_anuncio_candidato_atual != None:
                print(f'\nCandidatos RC:')
                print(df_anuncio.filter(self._lista_indice_anuncio_candidato_atual, axis=0))

            if candidato_selecionado != None:
                print('\nCandidato selecionado A_j:')
                print(df_anuncio.filter([candidato_selecionado], axis=0))

            print('\nSolução parcial S:')
            print(DataFrame(self.matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos']))

            print('\n==================================\n')

    def _solucao_vazia(self):
        matriz_solucao = []
        for _ in range(self.ambiente.quantidade_quadros):
            matriz_solucao.append([0, []])
        return matriz_solucao
