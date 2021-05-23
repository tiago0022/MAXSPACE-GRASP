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
        self._lista_quadro_disponivel = lista_quadro_disponivel
        self._espaco_total_ocupado = None
        self._proporcao_espaco_ocupado = None
        self._quantidade_quadros_completos = None
        self._criterio_desempate = None

    def _calcula_parametros_solucao(self):
        self._espaco_total_ocupado = 0
        self._quantidade_quadros_completos = 0
        for quadro in self.matriz_solucao:
            self._espaco_total_ocupado += quadro[0]
            self._quantidade_quadros_completos += int(quadro[0] == self.ambiente.tamanho_quadro)

    def espaco_total_ocupado(self):
        if self._espaco_total_ocupado == None:
            self._calcula_parametros_solucao()
        return self._espaco_total_ocupado

    def quantidade_quadros_completos(self):
        if self._quantidade_quadros_completos == None:
            self._calcula_parametros_solucao()
        return self._quantidade_quadros_completos

    def proporcao_espaco_ocupado(self):
        if self._proporcao_espaco_ocupado == None:
            self._proporcao_espaco_ocupado = self.espaco_total_ocupado() / self.ambiente.espaco_total
        return self._proporcao_espaco_ocupado

    def criterio_desempate(self):
        if self._criterio_desempate == None:
            self._criterio_desempate = self.quantidade_quadros_completos()
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
        copia._lista_quadro_disponivel = copy.deepcopy(self._lista_quadro_disponivel)
        copia._espaco_total_ocupado = self._espaco_total_ocupado
        copia._proporcao_espaco_ocupado = self._proporcao_espaco_ocupado
        copia._quantidade_quadros_completos = self._quantidade_quadros_completos
        copia._criterio_desempate = self._criterio_desempate
        return copia

    def __str__(self):
        df_solucao = DataFrame(self.matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos'])
        return df_solucao.__str__()

    def adiciona_ff(self, anuncio, indice_anuncio):
        if(indice_anuncio in self.lista_anuncio_adicionado):
            # print(indice_anuncio, 'já adicionado')
            return None

        frequencia_anuncio = anuncio[FREQUENCIA]

        lista_indice_quadro_selecionado = []
        contagem_quadros = 0

        for indice_quadro in self._lista_quadro_disponivel:
            if pode_ser_inserido(self.matriz_solucao[indice_quadro], anuncio, indice_anuncio, self._matriz_conflito, self.ambiente.tamanho_quadro):
                lista_indice_quadro_selecionado.append(indice_quadro)
                contagem_quadros = contagem_quadros + 1
                if contagem_quadros == frequencia_anuncio:
                    nova_solucao = self.copia()
                    nova_solucao.insere_na_solucao(lista_indice_quadro_selecionado, anuncio, indice_anuncio)
                    # print(indice_anuncio, 'adicionado')
                    return nova_solucao

        # print(indice_anuncio, 'não cabe')
        return None

    def insere_na_solucao(self, lista_quadro_selecionado, anuncio, indice_anuncio):

        tamanho_anuncio = anuncio[TAMANHO]

        for indice_quadro in lista_quadro_selecionado:
            tamanho_atualizado = self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] + tamanho_anuncio
            self.matriz_solucao[indice_quadro][ESPACO_OCUPADO] = tamanho_atualizado
            self.matriz_solucao[indice_quadro][LISTA_INDICE_ANUNCIO].append(indice_anuncio)
            if tamanho_atualizado == self.ambiente.tamanho_quadro:
                self._lista_quadro_disponivel.remove(indice_quadro)

        self.lista_anuncio_adicionado.append(indice_anuncio)
