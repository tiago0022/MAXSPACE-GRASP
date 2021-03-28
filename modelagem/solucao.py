from __future__ import annotations

from pandas.core.frame import DataFrame

from modelagem.ambiente import Ambiente


class Solucao:

    def __init__(self, ambiente: Ambiente, matriz_solucao=[]):
        self.ambiente = ambiente
        self.matriz_solucao = matriz_solucao
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

    def __str__(self):
        df_solucao = DataFrame(self.matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos'])
        return df_solucao.__str__()
