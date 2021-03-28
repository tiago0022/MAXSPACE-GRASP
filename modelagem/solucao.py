from pandas.core.frame import DataFrame

from modelagem.ambiente import Ambiente


class Solucao:

    def __init__(self, ambiente: Ambiente, matriz_solucao=[]):
        self.ambiente = ambiente
        self.matriz_solucao = matriz_solucao
        self._espaco_total_ocupado = None
        self._proporcao_espaco_ocupado = None

    def espaco_total_ocupado(self):
        if self._espaco_total_ocupado != None:
            return self._espaco_total_ocupado
        self._espaco_total_ocupado = 0
        for quadro in self.matriz_solucao:
            self._espaco_total_ocupado += quadro[0]
        return self._espaco_total_ocupado

    def proporcao_espaco_ocupado(self):
        if self._proporcao_espaco_ocupado != None:
            return self._proporcao_espaco_ocupado
        self._proporcao_espaco_ocupado = self.espaco_total_ocupado() / self.ambiente.espaco_total
        return self._proporcao_espaco_ocupado

    def __str__(self):
        df_solucao = DataFrame(self.matriz_solucao, columns=['Espaço ocupado', 'Anúncios inseridos'])
        return df_solucao.__str__()
