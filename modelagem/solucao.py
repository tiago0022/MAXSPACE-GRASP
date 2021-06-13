from __future__ import annotations

import copy

from pandas.core.frame import DataFrame

from modelagem.ambiente import Ambiente
from modelagem.anuncio import FREQUENCIA, GANHO, TAMANHO
from modelagem.quadro import (ESPACO_OCUPADO, LISTA_INDICE_ANUNCIO,
                              pode_ser_inserido)


class Solucao:

    # Solução
    matriz_solucao = None

    # Indexação para otimizar
    lista_anuncio_adicionado = None
    lista_anuncio_disponivel = None
    lista_quadro_disponivel = None

    # Dados do problema
    _ambiente = None
    _matriz_conflito = None
    _matriz_anuncio = None

    # Métricas de avaliação
    _espaco_total_ocupado = None
    _proporcao_espaco_ocupado = None
    _quantidade_quadros_completos = None
    _soma_quadrado_espaco_livre = None

    def __init__(self, ambiente: Ambiente, matriz_conflito, matriz_anuncio):

        self._ambiente = ambiente
        self._matriz_conflito = matriz_conflito
        self._matriz_anuncio = matriz_anuncio

        self.matriz_solucao = self._solucao_vazia()

        self.lista_anuncio_adicionado = []
        self.lista_anuncio_disponivel = list(range(len(matriz_anuncio)))
        self.lista_quadro_disponivel = list(range(self._ambiente.quantidade_quadros))

    def _solucao_vazia(self):
        matriz_solucao = []
        for _ in range(self._ambiente.quantidade_quadros):
            matriz_solucao.append([0, []])
        return matriz_solucao

    def quadro(self, quadro):
        return self.matriz_solucao[quadro]

    def _calcula_parametros_solucao(self):
        self._espaco_total_ocupado = 0
        self._quantidade_quadros_completos = 0
        self._soma_quadrado_espaco_livre = 0
        for quadro in self.matriz_solucao:
            espaco_ocupado = quadro[0]
            self._espaco_total_ocupado += espaco_ocupado
            self._quantidade_quadros_completos += int(quadro[0] == self._ambiente.tamanho_quadro)
            self._soma_quadrado_espaco_livre += ((self._ambiente.tamanho_quadro - espaco_ocupado) ** 2)

    def espaco_total_ocupado(self):
        if self._espaco_total_ocupado == None:
            self._calcula_parametros_solucao()
        return self._espaco_total_ocupado

    def quantidade_quadros_completos(self):
        if self._quantidade_quadros_completos == None:
            self._calcula_parametros_solucao()
        return self._quantidade_quadros_completos

    def soma_quadrado_espaco_livre(self):
        if self._soma_quadrado_espaco_livre == None:
            self._calcula_parametros_solucao()
        return self._soma_quadrado_espaco_livre

    def proporcao_espaco_ocupado(self):
        if self._proporcao_espaco_ocupado == None:
            self._proporcao_espaco_ocupado = self.espaco_total_ocupado() / self._ambiente.espaco_total
        return self._proporcao_espaco_ocupado

    def criterio_desempate(self):
        return self.soma_quadrado_espaco_livre()

    def ehMelhor(self, solucao: Solucao) -> bool:
        if self.espaco_total_ocupado() > solucao.espaco_total_ocupado():
            return True
        if self.espaco_total_ocupado() < solucao.espaco_total_ocupado():
            return False
        return self.criterio_desempate() > solucao.criterio_desempate()

    def copia(self) -> Solucao:
        copia = Solucao(self._ambiente, self._matriz_conflito, self._matriz_anuncio)

        copia.matriz_solucao = copy.deepcopy(self.matriz_solucao)

        copia.lista_anuncio_adicionado = copy.deepcopy(self.lista_anuncio_adicionado)
        copia.lista_quadro_disponivel = copy.deepcopy(self.lista_quadro_disponivel)
        copia.lista_anuncio_disponivel = copy.deepcopy(self.lista_anuncio_disponivel)

        copia._espaco_total_ocupado = self._espaco_total_ocupado
        copia._proporcao_espaco_ocupado = self._proporcao_espaco_ocupado
        copia._quantidade_quadros_completos = self._quantidade_quadros_completos
        copia._soma_quadrado_espaco_livre = self._soma_quadrado_espaco_livre

        return copia

    def __str__(self):
        df_solucao = DataFrame(self.matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos'])
        return df_solucao.__str__()

    # i deve estar fora da solução
    def adiciona(self, i) -> Solucao:

        anuncio = self._matriz_anuncio[i]
        frequencia_anuncio = anuncio[FREQUENCIA]

        lista_indice_quadro_selecionado = []
        contagem_quadros = 0

        for indice_quadro in self.lista_quadro_disponivel:
            if pode_ser_inserido(self.matriz_solucao[indice_quadro], anuncio, i, self._matriz_conflito, self._ambiente.tamanho_quadro):
                lista_indice_quadro_selecionado.append(indice_quadro)
                contagem_quadros = contagem_quadros + 1
                if contagem_quadros == frequencia_anuncio:
                    nova_solucao = self.copia()
                    nova_solucao.insere(lista_indice_quadro_selecionado, i)
                    # print(i, 'adicionado')
                    return nova_solucao

        # print(i, 'não cabe')
        return None

    # i deve estar na solução, j deve estar fora da solução
    def substitui(self, i, j) -> Solucao:

        anuncio_i = self._matriz_anuncio[i]
        anuncio_j = self._matriz_anuncio[j]

        if anuncio_j[GANHO] < anuncio_i[GANHO]:
            return None

        frequencia_i = anuncio_i[FREQUENCIA]
        frequencia_j = anuncio_j[FREQUENCIA]

        lista_indice_quadro_selecionado_i = []
        lista_indice_quadro_selecionado_j = []

        contagem_quadros_i = frequencia_i
        contagem_quadros_j = 0

        # print('Início tentativa: remover ', i, 'e adicionar', j)
        # print('Tamanho quadro:', self.ambiente.tamanho_quadro)
        # print(i, ': tamanho', anuncio_i[TAMANHO], '/ frequência', anuncio_i[FREQUENCIA])
        # print(j, ': tamanho', anuncio_j[TAMANHO], '/ frequência', anuncio_j[FREQUENCIA])
        # print()

        for indice_quadro in self._ambiente.lista_quadro():
            espaco_liberado = 0
            if contagem_quadros_i > 0 and self.anuncio_no_quadro(i, indice_quadro):
                # print('Remover de', indice_quadro, self.matriz_solucao[indice_quadro])
                lista_indice_quadro_selecionado_i.append(indice_quadro)
                contagem_quadros_i -= 1
                espaco_liberado = anuncio_i[TAMANHO]

            if contagem_quadros_j < frequencia_j and pode_ser_inserido(self.matriz_solucao[indice_quadro], anuncio_j, j, self._matriz_conflito, self._ambiente.tamanho_quadro, espaco_liberado, i):
                # print('Adicionar em', indice_quadro, self.matriz_solucao[indice_quadro])
                lista_indice_quadro_selecionado_j.append(indice_quadro)
                contagem_quadros_j += 1

            if contagem_quadros_j == frequencia_j and contagem_quadros_i == 0:
                # print('\nÉ possível fazer a alteração\n\n===================\n\n')
                nova_solucao = self.copia()
                nova_solucao._remove(lista_indice_quadro_selecionado_i, i)
                nova_solucao.insere(lista_indice_quadro_selecionado_j, j)
                return nova_solucao

        # print('\nNão é possível fazer a alteração\n\n===================\n\n')
        return None

    def remaneja(self, i, quadro_i, j, quadro_j) -> Solucao:

        if quadro_i == quadro_j or i == j:
            return None

        tamanho_i = self._matriz_anuncio[i][TAMANHO]
        tamanho_j = self._matriz_anuncio[j][TAMANHO]
        novo_espaco_quadro_i = self.matriz_solucao[quadro_i][ESPACO_OCUPADO] - tamanho_i
        novo_espaco_quadro_j = self.matriz_solucao[quadro_j][ESPACO_OCUPADO] - tamanho_j

        if novo_espaco_quadro_i < tamanho_j or novo_espaco_quadro_j < tamanho_i:
            return None

        if self.anuncio_no_quadro(i, quadro_j) or self.anuncio_no_quadro(j, quadro_i):
            return None

        nova_solucao = self.copia()

        nova_solucao._remove_copia(i, quadro_i)
        nova_solucao._remove_copia(j, quadro_j)

        nova_solucao._insere_copia(i, quadro_j)
        nova_solucao._insere_copia(j, quadro_i)

        return nova_solucao

    def anuncio_no_quadro(self, indice_anuncio, indice_quadro):
        lista_indice_anuncio = self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO]
        return indice_anuncio in lista_indice_anuncio

    def move(self, i, quadro_i, quadro_l) -> Solucao:
        if quadro_i == quadro_l:
            return None

        anuncio_i = self._matriz_anuncio[i]

        if pode_ser_inserido(self.matriz_solucao[quadro_l], anuncio_i, i, self._matriz_conflito, self._ambiente.tamanho_quadro):
            nova_solucao = self.copia()
            nova_solucao._remove_copia(i, quadro_i)
            nova_solucao._insere_copia(i, quadro_l)

        return None

    def insere(self, lista_quadro_selecionado, indice_anuncio):

        for indice_quadro in lista_quadro_selecionado:
            self._insere_copia(indice_anuncio, indice_quadro)

        self.lista_anuncio_adicionado.append(indice_anuncio)
        self.lista_anuncio_disponivel.remove(indice_anuncio)

    def _insere_copia(self, indice_anuncio, indice_quadro):
        tamanho_anuncio = self._matriz_anuncio[indice_anuncio][TAMANHO]
        tamanho_atualizado = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] + tamanho_anuncio
        self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = tamanho_atualizado
        self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].append(indice_anuncio)
        if tamanho_atualizado == self._ambiente.tamanho_quadro:
            self.lista_quadro_disponivel.remove(indice_quadro)

    def _remove(self, lista_quadro_selecionado, indice_anuncio):

        for indice_quadro in lista_quadro_selecionado:
            self._remove_copia(indice_anuncio, indice_quadro)

        self.lista_anuncio_adicionado.remove(indice_anuncio)
        self.lista_anuncio_disponivel.append(indice_anuncio)

    def _remove_copia(self, indice_anuncio, indice_quadro):
        tamanho_anuncio = self._matriz_anuncio[indice_anuncio][TAMANHO]
        tamanho_atualizado = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] - tamanho_anuncio
        self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = tamanho_atualizado
        self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].remove(indice_anuncio)
        if tamanho_atualizado == (self._ambiente.tamanho_quadro - tamanho_anuncio):
            self.lista_quadro_disponivel.append(indice_quadro)
