import time
import numpy as np

EXIBE_TEMPO = 1  # padrão = False


class RegistroTempo:

    def __init__(self, descricao='.', inicializa_agora=True):
        self.descricao = descricao
        self.inicio = None
        self.fim = None
        if inicializa_agora:
            self.inicializa()

    def exibe(self, nova_linha=False, ignora_inativacao=False):
        if EXIBE_TEMPO or ignora_inativacao:
            if self.fim is None:
                self.finaliza()

            texto = self.descricao + '..'
            while len(texto) < 35:
                texto = texto + '.'

            print(f'{texto}{round(self.fim - self.inicio, 3)} s')

            if nova_linha:
                print()

            return self.fim - self.inicio

    def exibe_soma(lista_tempo, descricao, nova_linha=False, ignora_inativacao=False):
        if EXIBE_TEMPO or ignora_inativacao:
            texto = descricao + '..'
            while len(texto) < 35:
                texto = texto + '.'

            tempo = np.sum(lista_tempo)
            print(f'{texto}{round(tempo, 3)} s')

            if nova_linha:
                print()

            return tempo

    def exibe_media(lista_tempo, descricao, nova_linha=False, ignora_inativacao=False):
        if EXIBE_TEMPO or ignora_inativacao:
            texto = descricao + '..'
            while len(texto) < 35:
                texto = texto + '.'

            tempo = np.average(lista_tempo)
            print(f'{texto}{round(tempo, 3)} s')

            if nova_linha:
                print()

            return tempo

    def exibe_quantidade(lista_tempo, descricao, nova_linha=False, ignora_inativacao=False):
        if EXIBE_TEMPO or ignora_inativacao:
            texto = descricao + '..'
            while len(texto) < 35:
                texto = texto + '.'

            tempo = len(lista_tempo)
            print(f'{texto}{round(tempo, 3)} iterações')

            if nova_linha:
                print()

            return tempo

    def inicializa(self):
        self.inicio = time.time()
        self.fim = None

    def finaliza(self):
        self.fim = time.time()
        return self.fim - self.inicio

    def tempo(self):
        return self.fim - self.inicio
