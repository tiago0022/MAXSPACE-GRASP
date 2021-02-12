import random as rd
import sys

from grasp.grasp import grasp

# Parâmetros padrão
caminho_instancia = 'instancias/basico/'
alpha = 0.25
seed = 1

# Leitura dos parâmetros de entrada
for i in range(1, len(sys.argv) , 2):
    if sys.argv[i] == '-p':
        caminho_instancia = sys.argv[i+1]
    if sys.argv[i] == '-a':
        alpha = float(sys.argv[i+1])
    if sys.argv[i] == '-s':
        seed = int(sys.argv[i+1])

rd.seed(seed)

grasp(caminho_instancia, alpha, seed)