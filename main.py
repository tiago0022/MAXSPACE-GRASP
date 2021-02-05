import sys
from estrutura_dados.leitor_entrada import obtemInstancia

caminhoInstancia = 'instancias/basico'

if len(sys.argv) >= 2:
    caminhoInstancia = sys.argv[1]

dfAnuncio, dfConflito, tamanhoQuadro, quantidadeQuadros = obtemInstancia(caminhoInstancia)

print(f"Anúncios A_i:\n{dfAnuncio}\n\nConflitos C_ij:\n{dfConflito}\n\nTamanho do quadro L: {tamanhoQuadro}\nQuantidade de quadros B: {quantidadeQuadros}\n")
