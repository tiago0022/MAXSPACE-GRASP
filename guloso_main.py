import random as rd
import sys
import time

from guloso.guloso import Guloso

# Parâmetros padrão
caminho_instancia = 'instancias/basico/'
seed = int(time.time())
apenas_exibe_ajuda = False
ignora_conflitos = False

# Leitura dos parâmetros de entrada
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == '-p':
        caminho_instancia = sys.argv[i+1]
    if sys.argv[i] == '-s':
        seed = int(sys.argv[i+1])
    if sys.argv[i] == '-h':
        apenas_exibe_ajuda = True
    if sys.argv[i] == '-c':
        ignora_conflitos = bool(sys.argv[i+1])


def exibe_parametros():
    print('-p: Caminho da instância')
    print('-s: Semente da aleatoriedade')
    print('-c: Ignora conflitos')
    print('-h: Ajuda')


def executa():
    rd.seed(seed)
    Guloso(caminho_instancia, ignora_conflitos).soluciona()


if apenas_exibe_ajuda:
    exibe_parametros()
else:
    executa()
