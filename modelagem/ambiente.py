class Ambiente:

    def __init__(self, tamanho_quado, quantidade_quadros):
        self.tamanho_quadro = int(tamanho_quado)
        self.quantidade_quadros = int(quantidade_quadros)
        self.espaco_total = self.tamanho_quadro * self.quantidade_quadros
        self._lista_quadro = None

    def lista_quadro(self):
        if self._lista_quadro is None:
            self._lista_quadro = range(self.quantidade_quadros)
        return self._lista_quadro


def exibe_tamanho_quadro(ambiente: Ambiente):
    print('Tamanho quadro:', ambiente.tamanho_quadro)
