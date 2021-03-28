
import random as rd

import numpy as np
from modelagem.ambiente import Ambiente
from modelagem.anuncio import FREQUENCIA, GANHO, TAMANHO
from modelagem.quadro import (ESPACO_OCUPADO, LISTA_INDICE_ANUNCIO,
                              pode_ser_inserido)
from modelagem.solucao import Solucao
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

        self._lista_anuncio_disponivel = None
        self._lista_quadro_disponivel = None

        self._tempo_construcao = None
        self._lista_tempo_iteracao = None
        self._tempo_total_limites = None
        self._tempo_total_candidato = None
        self._tempo_total_first_fit = None

        self._limite_inferior_atual = None
        self._menor_ganho_atual = None
        self._maior_ganho_atual = None
        self._lista_indice_anuncio_candidato_atual = None
        self._tamanho_lista_indice_anuncio_candidato_atual = None

    def _limpa_construcao(self):
        self._tempo_construcao = RegistroTempo('Construção')
        tempo = RegistroTempo('Limpar solução anterior')
        self.matriz_solucao = self._solucao_vazia()
        self._lista_anuncio_disponivel = list(range(self.quantidade_anuncios))
        self._lista_quadro_disponivel = list(range(self.ambiente.quantidade_quadros))
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
        self._lista_tempo_iteracao = [0] * self.quantidade_anuncios
        self._tempo_total_limites = 0
        self._tempo_total_candidato = 0
        self._tempo_total_first_fit = 0

    def constroi(self, aleatoriedade) -> Solucao:

        self._limpa_construcao()

        self._exibe_iteracao()

        for iteracao in range(self.quantidade_anuncios):

            tempo_iteracao = RegistroTempo()

            self._atualiza_limite_inferior_atual(aleatoriedade)

            indice_selecionado = self._obtem_candidato()

            self._insere_first_fit(indice_selecionado)

            self._exibe_iteracao(iteracao, indice_selecionado)

            self._lista_anuncio_disponivel.remove(indice_selecionado)

            self._lista_tempo_iteracao[iteracao] = tempo_iteracao.finaliza()

        self._exibe_dados_tempo()

        return Solucao(self.ambiente, self.matriz_solucao)

    def _obtem_candidato(self):

        tempo_candidatos = RegistroTempo()

        if self._lista_indice_anuncio_candidato_atual == None:
            self._atualiza_lista_indice_anuncio_candidato()

        indice_selecionado = self._escolhe_candidato()

        self._tempo_total_candidato = self._tempo_total_candidato + tempo_candidatos.finaliza()

        return indice_selecionado

    def _atualiza_limite_inferior_atual(self, aleatoriedade):

        tempo_limites = RegistroTempo()

        if self._maior_ganho_atual == None or self._menor_ganho_atual == None or self._limite_inferior_atual == None:

            self._atualiza_menor_e_maior_ganhos_disponiveis_atuais()

            self._limite_inferior_atual = self._maior_ganho_atual - aleatoriedade * (self._maior_ganho_atual - self._menor_ganho_atual)

            self._lista_indice_anuncio_candidato_atual = None

        self._tempo_total_limites = self._tempo_total_limites + tempo_limites.finaliza()

    def _exibe_dados_tempo(self):
        if EXIBE_TEMPO:
            print(f'\nQuantidade de iterações: {self.quantidade_anuncios}\n')

            print(f'Média por iteração: {round(np.average(self._lista_tempo_iteracao) * 100, 1)} ms')
            print(f'Iteração mais rápida: {round(np.min(self._lista_tempo_iteracao) * 100, 1)} ms')
            print(f'Iteração mais lenta: {round(np.max(self._lista_tempo_iteracao) * 100, 1)} ms\n')

            print(f'Tempo total limites: {round(self._tempo_total_limites, 2)} s')
            print(f'Tempo total candidatos: {round(self._tempo_total_candidato, 2)} s')
            print(f'Tempo total first fit: {round(self._tempo_total_first_fit, 2)} s\n')

            self._tempo_construcao.exibe(1)

    def _atualiza_menor_e_maior_ganhos_disponiveis_atuais(self):

        tempo = RegistroTempo('Obter limites de ganho')
        menor_ganho = self.matriz_anuncio[self._lista_anuncio_disponivel[0]][GANHO]
        maior_ganho = self.matriz_anuncio[self._lista_anuncio_disponivel[0]][GANHO]

        for i in self._lista_anuncio_disponivel[1:]:
            ganho = self.matriz_anuncio[i][GANHO]
            if ganho < menor_ganho:
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
        for i in self._lista_anuncio_disponivel:
            anuncio = self.matriz_anuncio[i]
            if anuncio[GANHO] >= self._limite_inferior_atual:
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

    def _insere_first_fit(self, indice_candidato):

        tempo = RegistroTempo('First Fit')
        candidato = self.matriz_anuncio[indice_candidato]
        frequencia_anuncio = candidato[FREQUENCIA]

        lista_indice_quadro_selecionado = []
        contagem_quadros = 0

        for indice_quadro in self._lista_quadro_disponivel:
            if pode_ser_inserido(self.matriz_solucao[indice_quadro], candidato, indice_candidato, self.matriz_conflito, self.ambiente.tamanho_quadro):
                lista_indice_quadro_selecionado.append(indice_quadro)
                contagem_quadros = contagem_quadros + 1
                if contagem_quadros == frequencia_anuncio:
                    self._insere_na_solucao(lista_indice_quadro_selecionado, candidato, indice_candidato)
                    break

        self._tempo_total_first_fit = self._tempo_total_first_fit + tempo.finaliza()
        # tempo.exibe(1)

    def _insere_na_solucao(self, lista_quadro_selecionado, anuncio, indice_anuncio):

        tempo = RegistroTempo('Inserir na solução')
        tamanho_anuncio = anuncio[TAMANHO]

        for indice_quadro in lista_quadro_selecionado:
            tamanho_atualizado = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] + tamanho_anuncio
            self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = tamanho_atualizado
            self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].append(indice_anuncio)
            if tamanho_atualizado == self.ambiente.tamanho_quadro:
                self._lista_quadro_disponivel.remove(indice_quadro)

        # tempo.exibe(1)

    def _exibe_iteracao(self, iteracao=None, candidato_selecionado=None):
        if EXIBE_ITERACAO:

            if iteracao != None:
                print(f'\nIteração {iteracao + 1}:')

            df_anuncio = DataFrame(self.matriz_anuncio, columns=['Tamanho', 'Frequencia', 'Ganho'])

            print('\nAnúncios disponíveis C:')
            print(df_anuncio.filter(self._lista_anuncio_disponivel, axis=0))

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
