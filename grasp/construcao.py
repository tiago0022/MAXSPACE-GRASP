
import modelagem.anuncio as anuncio
from pandas import DataFrame


def constroi(df_anuncio: DataFrame, df_conflito, tamanho_quadro, quantidade_quadros, aleatoriedade, seed=1):

    df_solucao = DataFrame(columns=['indice_quadro', 'indice_anuncio'])
    df_anuncio = anuncio.calcula_ganho(df_anuncio)
    df_anuncio_disponivel = df_anuncio.copy()

    iteracao = 0
    while not df_anuncio_disponivel.empty:
    
        menor_custo = df_anuncio_disponivel['ganho'].min()
        maior_custo = df_anuncio_disponivel['ganho'].max()
        limite_inferior = maior_custo - aleatoriedade * (maior_custo - menor_custo)
        
        df_candidato: DataFrame = df_anuncio_disponivel.get(df_anuncio_disponivel['ganho'] >= limite_inferior)
        candidato_selecionado: DataFrame = df_candidato.sample(random_state=seed)

        # exibe_iteracao(iteracao, df_anuncio_disponivel, limite_inferior, df_candidato, candidato_selecionado)
        
        df_anuncio_disponivel.drop(candidato_selecionado.index, inplace=True)

        iteracao = iteracao + 1

        
def exibe_iteracao(iteracao, df_anuncio_disponivel, limite_inferior, df_candidato, candidato_selecionado):
    print(f'Iteração {iteracao + 1}:\n\nAnúncios disponíveis C:')
    print(df_anuncio_disponivel)
    print(f'\nLimite inferior: {limite_inferior}\n\nCandidatos RC:')
    print(df_candidato)
    print('\nCandidato selecionado A_j:')
    print(candidato_selecionado)
    print('\n==================================\n')
