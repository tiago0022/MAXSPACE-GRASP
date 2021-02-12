
from modelagem.anuncio import calcula_ganho
from modelagem.quadro import pode_ser_inserido
from pandas import DataFrame


def constroi(df_anuncio: DataFrame, df_conflito, tamanho_quadro, quantidade_quadros, aleatoriedade, seed=1):

    df_solucao = solucao_vazia(quantidade_quadros)
    df_anuncio = calcula_ganho(df_anuncio)
    df_anuncio_disponivel = df_anuncio.copy()

    iteracao = 0
    while not df_anuncio_disponivel.empty:

        menor_custo = df_anuncio_disponivel['ganho'].min()
        maior_custo = df_anuncio_disponivel['ganho'].max()
        limite_inferior = maior_custo - aleatoriedade * (maior_custo - menor_custo)

        df_candidato: DataFrame = df_anuncio_disponivel.get(df_anuncio_disponivel['ganho'] >= limite_inferior)
        candidato_selecionado: DataFrame = df_candidato.sample(random_state=seed)

        # exibe_iteracao(iteracao, df_anuncio_disponivel, limite_inferior, df_candidato, candidato_selecionado, df_solucao)

        insere_first_fit(df_solucao, candidato_selecionado, df_conflito, tamanho_quadro)
        df_anuncio_disponivel.drop(candidato_selecionado.index, inplace=True)
        iteracao = iteracao + 1

    return df_solucao


def insere_first_fit(df_solucao: DataFrame, candidato: DataFrame, df_conflito, tamanho_quadro):

    frequencia_anuncio = candidato['frequencia'].values[0]

    lista_quadro_selecionado = []

    for indice_quadro, quadro in df_solucao.iterrows():
        if pode_ser_inserido(quadro, candidato, df_conflito, tamanho_quadro):
            lista_quadro_selecionado.append(indice_quadro)
        if len(lista_quadro_selecionado) == frequencia_anuncio:
            insere_na_solucao(df_solucao, lista_quadro_selecionado, candidato)
            break


def insere_na_solucao(df_solucao: DataFrame, lista_quadro_selecionado, anuncio: DataFrame):

    indice_anuncio = anuncio.first_valid_index()
    tamanho_anuncio = anuncio['tamanho'].values[0]

    for indice_quadro in lista_quadro_selecionado:
        df_solucao.at[indice_quadro, 'espaco_ocupado'] = df_solucao.at[indice_quadro, 'espaco_ocupado'] + tamanho_anuncio
        df_solucao.at[indice_quadro, 'lista_indice_anuncio'] = df_solucao.at[indice_quadro, 'lista_indice_anuncio'] + [indice_anuncio]


def exibe_iteracao(iteracao, df_anuncio_disponivel, limite_inferior, df_candidato, candidato_selecionado, df_solucao):
    print(f'Iteração {iteracao + 1}:\n\nAnúncios disponíveis C:')
    print(df_anuncio_disponivel)
    print(f'\nLimite inferior: {limite_inferior}\n\nCandidatos RC:')
    print(df_candidato)
    print('\nCandidato selecionado A_j:')
    print(candidato_selecionado)
    print('\nSolução parcial S:')
    print(df_solucao)
    print('\n==================================\n')


def solucao_vazia(quantidade_quadros):
    df_solucao = DataFrame({'quadro': range(1, quantidade_quadros + 1),
                            'espaco_ocupado': [0] * quantidade_quadros,
                            'lista_indice_anuncio': [[]] * quantidade_quadros
                            })
    return df_solucao.set_index('quadro')
