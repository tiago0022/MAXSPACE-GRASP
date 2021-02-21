import time


class RegistroTempo:

    def __init__(self, descricao, inicializa_agora=True):
        self.descricao = descricao
        self.inicio = None
        self.fim = None
        if inicializa_agora:
            self.inicializa()

    def exibe(self):

        if self.fim is None:
            self.finaliza()

        texto = self.descricao + '..'
        while len(texto) < 40:
            texto = texto + '.'

        print(f'{texto}{round(self.fim - self.inicio, 3)} s')

    def inicializa(self):
        self.inicio = time.time()

    def finaliza(self):
        self.fim = time.time()
