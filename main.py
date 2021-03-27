import random as rd
import sys
import time

from grasp.grasp import Grasp

# Parâmetros padrão
caminho_instancia = 'instancias/basico/'
quantidade_iteracoes = 50
seed = int(time.time())
apenas_exibe_ajuda = False

alpha = 0.25  # aleatoriedade da fase de construção

# Leitura dos parâmetros de entrada
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == '-p':
        caminho_instancia = sys.argv[i+1]
    if sys.argv[i] == '-a':
        alpha = float(sys.argv[i+1])
    if sys.argv[i] == '-s':
        seed = int(sys.argv[i+1])
    if sys.argv[i] == '-i':
        quantidade_iteracoes = int(sys.argv[i+1])
    if sys.argv[i] == '-h':
        apenas_exibe_ajuda = True


def exibe_parametros():
    print('-p: Caminho da instância')
    print('-a: Aleatoriedade alpha')
    print('-s: Semente da aleatoriedade')
    print('-i: Quantidade de iterações GRASP')
    print('-h: Ajuda')


if apenas_exibe_ajuda:
    exibe_parametros()
else:
    rd.seed(seed)

    Grasp(caminho_instancia, quantidade_iteracoes, alpha).soluciona()
