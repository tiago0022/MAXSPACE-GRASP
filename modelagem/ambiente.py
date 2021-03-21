class Ambiente:

    def __init__(self, tamanho_quado, quantidade_quadros):
        self.tamanho_quadro = int(tamanho_quado)
        self.quantidade_quadros = int(quantidade_quadros)
        self.espaco_total = self.tamanho_quadro * self.quantidade_quadros
