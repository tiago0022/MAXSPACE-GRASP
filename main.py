import random as rd
import sys
import time

from grasp.grasp import Grasp

# Parâmetros padrão
caminho_instancia = 'instancias/basico/'
quantidade_iteracoes = 50 
seed = int(time.time())

alpha = 0.25 # aleatoriedade da fase de construção

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


rd.seed(seed)

Grasp(caminho_instancia, quantidade_iteracoes, alpha).soluciona()
