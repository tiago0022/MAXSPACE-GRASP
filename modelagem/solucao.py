from __future__ import annotations
from modelagem.quadro import ESPACO_OCUPADO, LISTA_INDICE_ANUNCIO, pode_ser_inserido
from modelagem.anuncio import FREQUENCIA, TAMANHO

from pandas.core.frame import DataFrame
import copy
from modelagem.ambiente import Ambiente


class Solucao:

    def __init__(self, ambiente: Ambiente, matriz_conflito, matriz_solucao=[], lista_quadro_disponivel=[], lista_anuncio_adicionado=[]):
        self.ambiente = ambiente
        self.matriz_solucao = matriz_solucao
        self.lista_anuncio_adicionado = lista_anuncio_adicionado
        self._matriz_conflito = matriz_conflito
        self.lista_quadro_disponivel = lista_quadro_disponivel
        self._espaco_total_ocupado = None
        self._proporcao_espaco_ocupado = None
        self._quantidade_quadros_completos = None
        self._soma_quadrado_espaco_livre = None
        self._criterio_desempate = None

    def _calcula_parametros_solucao(self):
        self._espaco_total_ocupado = 0
        self._quantidade_quadros_completos = 0
        self._soma_quadrado_espaco_livre = 0
        for quadro in self.matriz_solucao:
            espaco_ocupado = quadro[0]
            self._espaco_total_ocupado += espaco_ocupado
            self._quantidade_quadros_completos += int(quadro[0] == self.ambiente.tamanho_quadro)
            self._soma_quadrado_espaco_livre += ((self.ambiente.tamanho_quadro - espaco_ocupado) ** 2)

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
            self._proporcao_espaco_ocupado = self.espaco_total_ocupado() / self.ambiente.espaco_total
        return self._proporcao_espaco_ocupado

    def criterio_desempate(self):
        if self._criterio_desempate == None:
            self._criterio_desempate = self.soma_quadrado_espaco_livre()
        return self._criterio_desempate

    def ehMelhor(self, solucao: Solucao) -> bool:
        if self.espaco_total_ocupado() > solucao.espaco_total_ocupado():
            return True
        if self.espaco_total_ocupado() < solucao.espaco_total_ocupado():
            return False
        return self.criterio_desempate() > solucao.criterio_desempate()

    def copia(self) -> Solucao:
        copia = Solucao(self.ambiente, self._matriz_conflito)
        copia.matriz_solucao = copy.deepcopy(self.matriz_solucao)
        copia.lista_anuncio_adicionado = copy.deepcopy(self.lista_anuncio_adicionado)
        copia.lista_quadro_disponivel = copy.deepcopy(self.lista_quadro_disponivel)
        copia._espaco_total_ocupado = self._espaco_total_ocupado
        copia._proporcao_espaco_ocupado = self._proporcao_espaco_ocupado
        copia._quantidade_quadros_completos = self._quantidade_quadros_completos
        copia._criterio_desempate = self._criterio_desempate
        return copia

    def __str__(self):
        df_solucao = DataFrame(self.matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos'])
        return df_solucao.__str__()

    def adiciona_ff(self, anuncio, indice_anuncio) -> Solucao:
        if(indice_anuncio in self.lista_anuncio_adicionado):
            # print(indice_anuncio, 'já adicionado')
            return None

        frequencia_anuncio = anuncio[FREQUENCIA]

        lista_indice_quadro_selecionado = []
        contagem_quadros = 0

        for indice_quadro in self.lista_quadro_disponivel:
            if pode_ser_inserido(self.matriz_solucao[indice_quadro], anuncio, indice_anuncio, self._matriz_conflito, self.ambiente.tamanho_quadro):
                lista_indice_quadro_selecionado.append(indice_quadro)
                contagem_quadros = contagem_quadros + 1
                if contagem_quadros == frequencia_anuncio:
                    nova_solucao = self.copia()
                    nova_solucao._insere(lista_indice_quadro_selecionado, anuncio, indice_anuncio)
                    # print(indice_anuncio, 'adicionado')
                    return nova_solucao

        # print(indice_anuncio, 'não cabe')
        return None

    def substitui(self, anuncio_i, i, anuncio_j, j) -> Solucao:
        if i not in self.lista_anuncio_adicionado or j in self.lista_anuncio_adicionado:
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

        for indice_quadro in self.ambiente.lista_quadro():
            espaco_liberado = 0
            if contagem_quadros_i > 0 and self.anuncio_no_quadro(i, indice_quadro):
                # print('Remover de', indice_quadro, self.matriz_solucao[indice_quadro])
                lista_indice_quadro_selecionado_i.append(indice_quadro)
                contagem_quadros_i -= 1
                espaco_liberado = anuncio_i[TAMANHO]

            if contagem_quadros_j < frequencia_j and pode_ser_inserido(self.matriz_solucao[indice_quadro], anuncio_j, j, self._matriz_conflito, self.ambiente.tamanho_quadro, espaco_liberado, i):
                # print('Adicionar em', indice_quadro, self.matriz_solucao[indice_quadro])
                lista_indice_quadro_selecionado_j.append(indice_quadro)
                contagem_quadros_j += 1

            if contagem_quadros_j == frequencia_j and contagem_quadros_i == 0:
                # print('\nÉ possível fazer a alteração\n\n===================\n\n')
                nova_solucao = self.copia()
                nova_solucao._remove(lista_indice_quadro_selecionado_i, anuncio_i, i)
                nova_solucao._insere(lista_indice_quadro_selecionado_j, anuncio_j, j)
                return nova_solucao

        # print('\nNão é possível fazer a alteração\n\n===================\n\n')
        return None

    def remaneja(self, anuncio_i, i, quadro_i, anuncio_j, j, quadro_j) -> Solucao:

        if quadro_i == quadro_j or i == j:
            return None

        tamanho_i = anuncio_i[TAMANHO]
        tamanho_j = anuncio_j[TAMANHO]
        novo_espaco_quadro_i = self.matriz_solucao[quadro_i][ESPACO_OCUPADO] - tamanho_i
        novo_espaco_quadro_j = self.matriz_solucao[quadro_j][ESPACO_OCUPADO] - tamanho_j

        if novo_espaco_quadro_i < tamanho_j or novo_espaco_quadro_j < tamanho_i:
            return None

        nova_solucao = self.copia()

        nova_solucao._remove_copia(i, tamanho_i, quadro_i)
        nova_solucao._remove_copia(j, tamanho_j, quadro_j)

        nova_solucao._insere_copia(i, tamanho_i, quadro_j)
        nova_solucao._insere_copia(j, tamanho_j, quadro_i)

        return nova_solucao

    def anuncio_no_quadro(self, indice_anuncio, indice_quadro):
        lista_indice_anuncio = self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO]
        return indice_anuncio in lista_indice_anuncio

    def move(self, anuncio_i, i, quadro_i, quadro_l) -> Solucao:
        if quadro_i == quadro_l:
            return None

        if pode_ser_inserido(self.matriz_solucao[quadro_l], anuncio_i, i, self._matriz_conflito, self.ambiente.tamanho_quadro):
            nova_solucao = self.copia()
            nova_solucao._remove_copia(i, anuncio_i[TAMANHO], quadro_i)
            nova_solucao._insere_copia(i, anuncio_i[TAMANHO], quadro_l)

        return None

    def _insere(self, lista_quadro_selecionado, anuncio, indice_anuncio):

        tamanho_anuncio = anuncio[TAMANHO]

        for indice_quadro in lista_quadro_selecionado:
            self._insere_copia(indice_anuncio, tamanho_anuncio, indice_quadro)

        self.lista_anuncio_adicionado.append(indice_anuncio)

    def _insere_copia(self, indice_anuncio, tamanho_anuncio, indice_quadro):
        tamanho_atualizado = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] + tamanho_anuncio
        self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = tamanho_atualizado
        self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].append(indice_anuncio)
        if tamanho_atualizado == self.ambiente.tamanho_quadro:
            self.lista_quadro_disponivel.remove(indice_quadro)

    def _remove(self, lista_quadro_selecionado, anuncio, indice_anuncio):

        tamanho_anuncio = anuncio[TAMANHO]

        for indice_quadro in lista_quadro_selecionado:
            self._remove_copia(indice_anuncio, tamanho_anuncio, indice_quadro)

        self.lista_anuncio_adicionado.remove(indice_anuncio)

    def _remove_copia(self, indice_anuncio, tamanho_anuncio, indice_quadro):
        tamanho_atualizado = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] - tamanho_anuncio
        self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = tamanho_atualizado
        self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].remove(indice_anuncio)
        if tamanho_atualizado == self.ambiente.tamanho_quadro - tamanho_anuncio:
            self.lista_quadro_disponivel.append(indice_quadro)
