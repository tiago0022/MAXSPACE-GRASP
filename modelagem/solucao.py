from __future__ import annotations

import copy

import numpy as np
from pandas.core.frame import DataFrame
from tempo_execucao import RegistroTempo

from modelagem.ambiente import Ambiente, exibe_tamanho_quadro
from modelagem.anuncio import FREQUENCIA, GANHO, TAMANHO, exibe_anuncio
from modelagem.quadro import ESPACO_OCUPADO, LISTA_INDICE_ANUNCIO, exibe_quadro


class Solucao:

    # Dados do problema
    _ambiente = None
    _matriz_conflito = None
    _matriz_anuncio = None

    # Solução
    matriz_solucao = None

    # Indexação para otimizar
    lista_anuncio_adicionado = None
    lista_anuncio_disponivel = None
    lista_quadro_disponivel = None
    matriz_anuncio_quadro = None
    quantidade_anuncios = None
    dicionario_espaco_quadro = None

    # Métricas de avaliação
    espaco_total_ocupado = None
    quantidade_quadros_completos = None
    soma_quadrado_espaco_livre = None

    def __init__(self, ambiente: Ambiente, matriz_conflito, matriz_anuncio, inicializa=True):

        # Dados do problema
        self._ambiente = ambiente
        self._matriz_conflito = matriz_conflito
        self._matriz_anuncio = matriz_anuncio

        if inicializa:

            # Solução
            self.matriz_solucao = self._matriz_solucao_vazia()

            # Indexação para otimizar
            self.quantidade_anuncios = len(matriz_anuncio)
            self.lista_anuncio_adicionado = []
            self.lista_anuncio_disponivel = list(range(self.quantidade_anuncios))
            self.lista_quadro_disponivel = list(range(self._ambiente.quantidade_quadros))
            self.matriz_anuncio_quadro = self._matriz_anuncio_quadro_vazia()
            self.dicionario_espaco_quadro = self._dicionario_espaco_quadro_vazio()

            # Métricas de avaliação
            self.espaco_total_ocupado = 0
            self.quantidade_quadros_completos = 0
            self.soma_quadrado_espaco_livre = (self._ambiente.tamanho_quadro ** 2) * self._ambiente.quantidade_quadros

    def copia(self) -> Solucao:

        copia = Solucao(self._ambiente, self._matriz_conflito, self._matriz_anuncio, False)

        # Solução
        copia.matriz_solucao = copy.deepcopy(self.matriz_solucao)

        # Indexação para otimizar
        copia.quantidade_anuncios = self.quantidade_anuncios
        copia.lista_anuncio_adicionado = copy.deepcopy(self.lista_anuncio_adicionado)
        copia.lista_quadro_disponivel = copy.deepcopy(self.lista_quadro_disponivel)
        copia.lista_anuncio_disponivel = copy.deepcopy(self.lista_anuncio_disponivel)
        copia.matriz_anuncio_quadro = copy.deepcopy(self.matriz_anuncio_quadro)
        copia.dicionario_espaco_quadro = copy.deepcopy(self.dicionario_espaco_quadro)

        # Métricas de avaliação
        copia.espaco_total_ocupado = self.espaco_total_ocupado
        copia.quantidade_quadros_completos = self.quantidade_quadros_completos
        copia.soma_quadrado_espaco_livre = self.soma_quadrado_espaco_livre

        return copia

    def criterio_desempate(self):
        return self.soma_quadrado_espaco_livre

    def _matriz_anuncio_quadro_vazia(self):
        matriz_anuncio_quadro = []
        for _ in range(self.quantidade_anuncios):
            matriz_anuncio_quadro.append([])
        return matriz_anuncio_quadro

    def _dicionario_espaco_quadro_vazio(self):
        dicionario_espaco_quadro = {self._ambiente.tamanho_quadro: list(range(self._ambiente.quantidade_quadros))}
        for tamanho in range(self._ambiente.tamanho_quadro):
            dicionario_espaco_quadro[tamanho] = []
        return dicionario_espaco_quadro

    def _matriz_solucao_vazia(self):
        matriz_solucao = []
        for _ in range(self._ambiente.quantidade_quadros):
            matriz_solucao.append([0, []])
        return matriz_solucao

    def quadro(self, quadro):
        return self.matriz_solucao[quadro]

    def proporcao_espaco_ocupado(self):
        return self.espaco_total_ocupado / self._ambiente.espaco_total

    def eh_melhor(self, solucao: Solucao) -> bool:
        if self.espaco_total_ocupado > solucao.espaco_total_ocupado:
            return True
        if self.espaco_total_ocupado < solucao.espaco_total_ocupado:
            return False
        return self.criterio_desempate() > solucao.criterio_desempate()

    def eh_otimo(self):
        return self.espaco_total_ocupado == self._ambiente.espaco_total

    def __str__(self):
        df_solucao = DataFrame(self.matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos'])
        return df_solucao.__str__() + f'\n\n{self.metricas()}'

    def metricas(self) -> str:
        return f'Espaço ocupado: {self.espaco_total_ocupado} ({self.porcentagem_espaco_ocupado()}%)\nCritério de desempate: {self.criterio_desempate()} \n'

    def porcentagem_espaco_ocupado(self):
        return np.round(self.proporcao_espaco_ocupado() * 100, 2)

    def avaliacao(self) -> str:
        return f'\nEspaço ocupado: {self.espaco_total_ocupado}/{self._ambiente.espaco_total} ({self.porcentagem_espaco_ocupado()}%)\n'

    # i deve estar fora da solução
    def adiciona(self, i) -> Solucao:

        anuncio = self._matriz_anuncio[i]
        frequencia_anuncio = anuncio[FREQUENCIA]

        lista_indice_quadro_selecionado = []
        contagem_quadros = 0

        for indice_quadro in self.lista_quadro_disponivel:
            if self.copia_pode_ser_inserida(i, indice_quadro):
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

        # print('Início tentativa: remover', i, 'e adicionar', j)
        # exibe_tamanho_quadro(self._ambiente)
        # exibe_anuncio(i, anuncio_i)
        # exibe_anuncio(j, anuncio_j)
        # print()

        if anuncio_j[GANHO] < anuncio_i[GANHO]:
            # print(f'O ganho de {j} ({anuncio_j[GANHO]}) é menor que o ganho de {i} ({anuncio_i[GANHO]})\n\n===================\n')
            return None

        contagem_quadros_j = 0
        frequencia_j = anuncio_j[FREQUENCIA]
        lista_indice_quadro_possivel_j = []

        espaco_liberado = anuncio_i[TAMANHO]

        for indice_quadro in self.matriz_anuncio_quadro[i]:
            if self.copia_pode_ser_inserida(j, indice_quadro, espaco_liberado, i):
                lista_indice_quadro_possivel_j.append(indice_quadro)
                contagem_quadros_j += 1
                # print('Remover de', indice_quadro, self.matriz_solucao[indice_quadro])
                # print('Adicionar em', indice_quadro, self.matriz_solucao[indice_quadro], f'({contagem_quadros_j} adicionados)')

        for indice_quadro in self.lista_quadro_disponivel:
            if self.copia_pode_ser_inserida(j, indice_quadro) and indice_quadro not in lista_indice_quadro_possivel_j:
                lista_indice_quadro_possivel_j.append(indice_quadro)
                contagem_quadros_j += 1
                # print('Adicionar em', indice_quadro, self.matriz_solucao[indice_quadro], f'({contagem_quadros_j} adicionados)')

        if contagem_quadros_j >= frequencia_j:
            # print('\nÉ possível fazer a alteração\n\n===================\n')

            lista_indice_quadro_possivel_j.sort()
            lista_quadro_selecionado_j = lista_indice_quadro_possivel_j[:frequencia_j]

            nova_solucao = self.copia()
            nova_solucao._remove(self.matriz_anuncio_quadro[i], i)
            nova_solucao.insere(lista_quadro_selecionado_j, j)
            return nova_solucao

        # print('\nNão é possível fazer a alteração\n\n===================\n')
        return None

    # i e j devem estar na solução, nos respectivos quadros i e j
    def remaneja(self, i, quadro_i, j, quadro_j) -> Solucao:

        # print('Início tentativa: trocar a cópia de', i, 'no quadro', quadro_i, 'pela cópia de', j, 'no quadro', quadro_j)
        # exibe_tamanho_quadro(self._ambiente)
        # exibe_anuncio(i, self._matriz_anuncio[i])
        # exibe_anuncio(j, self._matriz_anuncio[j])
        # exibe_quadro(quadro_i, self.matriz_solucao[quadro_i])
        # exibe_quadro(quadro_j, self.matriz_solucao[quadro_j])
        # print()

        if quadro_i == quadro_j or i == j:
            # print('Alteração redundante\n\n===================\n')
            return None

        tamanho_i = self._matriz_anuncio[i][TAMANHO]
        tamanho_j = self._matriz_anuncio[j][TAMANHO]

        if self.copia_pode_ser_inserida(i, quadro_j, tamanho_j, j) and self.copia_pode_ser_inserida(j, quadro_i, tamanho_i, i):
            # print('\nÉ possível fazer a alteração')

            if not self._remaneja_gera_melhora(quadro_i, quadro_j, tamanho_i, tamanho_j):
                # print('\nAlteração não compensa\n\n===================\n')
                return None

            # print('\nAlteração realizada\n\n===================\n')
            nova_solucao = self.copia()

            nova_solucao._remove_copia(i, quadro_i)
            nova_solucao._remove_copia(j, quadro_j)

            nova_solucao._insere_copia(i, quadro_j)
            nova_solucao._insere_copia(j, quadro_i)

            return nova_solucao

        # print('\nNão é possível fazer a alteração\n\n===================\n')
        return None

    def _remaneja_gera_melhora(self, quadro_i, quadro_j, tamanho_i, tamanho_j):

        espaco_livre_i = self._espaco_livre(quadro_i)
        espaco_livre_j = self._espaco_livre(quadro_j)

        termo_remove_i = self.termo_remove_copia(tamanho_i, espaco_livre_i)
        termo_remove_j = self.termo_remove_copia(tamanho_j, espaco_livre_j)
        termo_insere_i = self.termo_insere_copia(tamanho_i, espaco_livre_j)
        termo_insere_j = self.termo_insere_copia(tamanho_j, espaco_livre_i)

        return (termo_remove_i + termo_remove_j + termo_insere_i + termo_insere_j) > 0

    def anuncio_no_quadro(self, indice_anuncio, indice_quadro):
        lista_indice_anuncio = self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO]
        return indice_anuncio in lista_indice_anuncio

    # i deve estar na solução, no quadro i, k deve estar disponível
    def move(self, i, quadro_i, quadro_k) -> Solucao:

        # print('Início tentativa: mover cópia de', i, 'do quadro', quadro_i, 'para o quadro', quadro_k)
        # exibe_tamanho_quadro(self._ambiente)
        # exibe_anuncio(i, self._matriz_anuncio[i])
        # exibe_quadro(quadro_i, self.matriz_solucao[quadro_i])
        # exibe_quadro(quadro_k, self.matriz_solucao[quadro_k])
        # print()

        if self.anuncio_no_quadro(i, quadro_k):
            # print(i, 'já está no quadro', quadro_k, '\n\n===================\n')
            return None

        if self.copia_pode_ser_inserida(i, quadro_k):
            # print('Alteração é possível')

            if not self._move_gera_melhora(i, quadro_i, quadro_k):
                # print('Alteração não compensa\n\n===================\n')
                return None

            # print(i, 'movido de', quadro_i, 'para', quadro_k, '\n\n===================\n')
            nova_solucao = self.copia()
            nova_solucao._remove_copia(i, quadro_i)
            nova_solucao._insere_copia(i, quadro_k)
            return nova_solucao

        # print('Não é possível fazer a alteração \n\n===================\n')
        return None

    def _move_gera_melhora(self, i, quadro_i, quadro_k):

        tamanho_i = self._matriz_anuncio[i][TAMANHO]

        espaco_livre_i = self._espaco_livre(quadro_i)
        espaco_livre_k = self._espaco_livre(quadro_k)

        termo_remove_i = self.termo_remove_copia(tamanho_i, espaco_livre_i)
        termo_insere_k = self.termo_insere_copia(tamanho_i, espaco_livre_k)

        return (termo_remove_i + termo_insere_k) > 0

    def _espaco_livre(self, quadro):
        return self._ambiente.tamanho_quadro - self.matriz_solucao[quadro][ESPACO_OCUPADO]

    def insere(self, lista_quadro_selecionado, indice_anuncio):

        for indice_quadro in lista_quadro_selecionado:
            self._insere_copia(indice_anuncio, indice_quadro)

        self.lista_anuncio_adicionado.append(indice_anuncio)
        self.lista_anuncio_disponivel.remove(indice_anuncio)

    def _insere_copia(self, indice_anuncio, indice_quadro):

        # Variáveis
        tamanho_anuncio = self._matriz_anuncio[indice_anuncio][TAMANHO]
        espaco_ocupado_anterior = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO]
        espaco_ocupado_atualizado = espaco_ocupado_anterior + tamanho_anuncio
        espaco_livre_anterior = self._espaco_livre(indice_quadro)
        espaco_livre_atualizado = self._ambiente.tamanho_quadro - espaco_ocupado_atualizado

        # Atualização dos dados
        self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = espaco_ocupado_atualizado
        self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].append(indice_anuncio)

        # Indexação
        self.matriz_anuncio_quadro[indice_anuncio].append(indice_quadro)

        if espaco_ocupado_atualizado == self._ambiente.tamanho_quadro:
            self.lista_quadro_disponivel.remove(indice_quadro)
            self.quantidade_quadros_completos += 1

        self.espaco_total_ocupado = self.espaco_total_ocupado + tamanho_anuncio
        self.soma_quadrado_espaco_livre = self.soma_quadrado_espaco_livre + self.termo_insere_copia(tamanho_anuncio, espaco_livre_anterior)
        self.dicionario_espaco_quadro[espaco_livre_anterior].remove(indice_quadro)
        self.dicionario_espaco_quadro[espaco_livre_atualizado].append(indice_quadro)

    def termo_insere_copia(self, tamanho_anuncio, espaco_livre_anterior):
        return (- 2 * espaco_livre_anterior * tamanho_anuncio) + (tamanho_anuncio ** 2)

    def _remove(self, lista_quadro_selecionado, indice_anuncio):

        for indice_quadro in lista_quadro_selecionado:
            self._remove_copia(indice_anuncio, indice_quadro)

        self.lista_anuncio_adicionado.remove(indice_anuncio)
        self.lista_anuncio_disponivel.append(indice_anuncio)

    def _remove_copia(self, indice_anuncio, indice_quadro):

        # Variáveis
        tamanho_anuncio = self._matriz_anuncio[indice_anuncio][TAMANHO]
        espaco_ocupado_anterior = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO]
        espaco_ocupado_atualizado = espaco_ocupado_anterior - tamanho_anuncio
        espaco_livre_anterior = self._espaco_livre(indice_quadro)
        espaco_livre_atualizado = self._ambiente.tamanho_quadro - espaco_ocupado_atualizado

        # Atualização dos dados
        self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = espaco_ocupado_atualizado
        self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].remove(indice_anuncio)

        # Indexação
        self.matriz_anuncio_quadro[indice_anuncio].remove(indice_quadro)

        if espaco_ocupado_anterior == self._ambiente.tamanho_quadro:
            self.lista_quadro_disponivel.append(indice_quadro)
            self.quantidade_quadros_completos -= 1

        self.espaco_total_ocupado = self.espaco_total_ocupado - tamanho_anuncio
        self.soma_quadrado_espaco_livre = self.soma_quadrado_espaco_livre + self.termo_remove_copia(tamanho_anuncio, espaco_livre_anterior)
        self.dicionario_espaco_quadro[espaco_livre_anterior].remove(indice_quadro)
        self.dicionario_espaco_quadro[espaco_livre_atualizado].append(indice_quadro)

    def termo_remove_copia(self, tamanho_anuncio, espaco_livre_anterior):
        return (2 * espaco_livre_anterior * tamanho_anuncio) + (tamanho_anuncio ** 2)

    def copia_pode_ser_inserida(self, indice_anuncio, indice_quadro, espaco_liberado=0, anuncio_liberado=None) -> bool:

        anuncio = self._matriz_anuncio[indice_anuncio]
        quadro = self.matriz_solucao[indice_quadro]

        tamanho_anuncio = anuncio[TAMANHO]
        espaco_ocupado = quadro[ESPACO_OCUPADO] - espaco_liberado
        lista_anuncio_ja_inserido = quadro[LISTA_INDICE_ANUNCIO]

        if espaco_ocupado + tamanho_anuncio > self._ambiente.tamanho_quadro:
            return False

        for anuncio_ja_inserido in lista_anuncio_ja_inserido:
            if anuncio_ja_inserido == anuncio_liberado:
                continue
            if self._existe_conflito(indice_anuncio, anuncio_ja_inserido):
                return False
            if indice_anuncio == anuncio_ja_inserido:
                return False

        # tempo.exibe()
        return True

    def _existe_conflito(self, i, j):
        if i < j:
            return self._matriz_conflito[j][i]
        return self._matriz_conflito[i][j]
