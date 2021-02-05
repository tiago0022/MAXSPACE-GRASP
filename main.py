import sys
from estrutura_dados.leitor_entrada import obtem_instancia

caminho_instancia = 'instancias/basico/'

if len(sys.argv) >= 2:
    caminho_instancia = sys.argv[1][:-1]

df_anuncio, df_conflito, tamanho_quadro, quantidade_quadros = obtem_instancia(caminho_instancia)

print(f"Tamanho do quadro L: {tamanho_quadro}\nQuantidade de quadros B: {quantidade_quadros}\n\nAnúncios A_i:\n{df_anuncio}\n\nConflitos C_ij:\n{df_conflito}\n")
