import sys
from estrutura_dados.leitor_entrada import obtem_instancia

caminho_instancia = 'instancias/basico'

if len(sys.argv) >= 2:
    caminho_instancia = sys.argv[1]

df_anuncio, df_conflito, tamanho_quadro, quantidade_quadros = obtem_instancia(caminho_instancia)

# print(f"Anúncios A_i:\n{dfAnuncio}\n\nConflitos C_ij:\n{dfConflito}\n\nTamanho do quadro L: {tamanhoQuadro}\nQuantidade de quadros B: {quantidadeQuadros}\n")
