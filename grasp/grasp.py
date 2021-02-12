from estrutura_dados.leitura_entrada import obtem_instancia

from grasp.construcao import constroi


def grasp(caminho_instancia, alpha, seed=1):

    df_anuncio, df_conflito, tamanho_quadro, quantidade_quadros = obtem_instancia(caminho_instancia)

    # print(f"Tamanho do quadro L: {tamanho_quadro}\nQuantidade de quadros B: {quantidade_quadros}\n\nAnúncios A_i:\n{df_anuncio}\n\nConflitos C_ij:\n{df_conflito}\n")

    df_solucao_construida = constroi(df_anuncio, df_conflito, tamanho_quadro, quantidade_quadros, alpha, seed)

    porcentagem_espaco_ocupado = (df_solucao_construida['espaco_ocupado'].sum() / (tamanho_quadro * quantidade_quadros)) * 100
    print(f'Solução construída:\n{df_solucao_construida}\n\nEspaço ocupado: {round(porcentagem_espaco_ocupado,2)}%')
