import time

EXIBE_TEMPO = 1  # padrão = False


class RegistroTempo:

    def __init__(self, descricao, inicializa_agora=True):
        self.descricao = descricao
        self.inicio = None
        self.fim = None
        if inicializa_agora:
            self.inicializa()

    def exibe(self, nova_linha=False, ignora_inativacao=False):

        if self.fim is None:
            self.finaliza()

        texto = self.descricao + '..'
        while len(texto) < 40:
            texto = texto + '.'

        if EXIBE_TEMPO or ignora_inativacao:
            print(f'{texto}{round(self.fim - self.inicio, 3)} s')
            if nova_linha:
                print()

        return self.fim - self.inicio

    def inicializa(self):
        self.inicio = time.time()

    def finaliza(self):
        self.fim = time.time()
        return self.fim - self.inicio
