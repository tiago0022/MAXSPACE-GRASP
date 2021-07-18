import random as rd
import time

import pandas as pd

from grasp.grasp import Grasp

nome_arquivo = 'resultados/instancias.csv'

INSTANCIA = 'Instância'
COM_CONFLITOS = 'Com conflitos'
ORDEM = 'Ordem'
EXECUTOU = 'Executou'
ANUNCIOS = 'Anúncios'
QUADROS = 'Quadros'
CONFLITOS = 'Conflitos'
TAMANHO_QUADRO = 'Tamanho quadro'
ESPACO_OCUPADO = 'Espaço ocupado'
METRICA = 'Métrica'
TEMPO = 'Tempo'
MELHOR_ITERACAO = 'Melhor iteração'
SOLUCAO = 'Solução'

quantidade_iteracoes = 100
alpha = 0.25

rd.seed(int(time.time()))

df = pd.read_csv(nome_arquivo, dtype={EXECUTOU: str, SOLUCAO: str})

for i, linha in df.iterrows():

    if linha[EXECUTOU] == 'S':
        continue

    caminho_instancia = linha[INSTANCIA]
    ignora_conflitos = (linha[COM_CONFLITOS] == 'N')

    grasp = Grasp(caminho_instancia, quantidade_iteracoes, alpha, ignora_conflitos)
    solucao = grasp.soluciona()

    df.at[i, ANUNCIOS] = solucao.quantidade_anuncios
    df.at[i, QUADROS] = solucao._ambiente.quantidade_quadros
    df.at[i, TAMANHO_QUADRO] = solucao._ambiente.tamanho_quadro
    df.at[i, ESPACO_OCUPADO] = solucao.espaco_total_ocupado
    df.at[i, METRICA] = solucao.criterio_desempate()
    df.at[i, TEMPO] = grasp.tempo_total.tempo()
    df.at[i, MELHOR_ITERACAO] = grasp.melhor_iteracao

    local_solucao = f'resultados/solucoes/{caminho_instancia[:-1]}_{linha[COM_CONFLITOS]}_solucao_{linha[ORDEM]}.csv'
    grasp.salva_solucao(local_solucao)
    df.at[i, SOLUCAO] = local_solucao

    df.at[i, EXECUTOU] = 'S'

    df.to_csv(nome_arquivo, index=False)
