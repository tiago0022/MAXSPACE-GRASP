import csv

lista_instancia = ['Aleatorio/aleatorio_pequeno_',
                   'Aleatorio/aleatorio_medio_',
                   'Aleatorio/aleatorio_grande_',
                   'Aleatorio/aleatorio_gigante_',
                   'Falkenauer_T/falkenauer_t60_',
                   'Falkenauer_T/falkenauer_t120_',
                   'Falkenauer_T/falkenauer_t249_',
                   'Falkenauer_T/falkenauer_t501_',
                   'Falkenauer_U/falkenauer_u120_',
                   'Falkenauer_U/falkenauer_u250_',
                   'Falkenauer_U/falkenauer_u500_',
                   'Falkenauer_U/falkenauer_u1000_']

lista_instancia_multiconflito = [10, 30, 50, 70]


arquivo = open(f'resultados/instancias_vazio.csv', 'w+')
arquivo_csv = csv.writer(arquivo)
arquivo_csv.writerow(['Instância', 'Com conflitos', 'Conflitos', 'Ordem', 'Executou', 'Anúncios', 'Quadros', 'Tamanho quadro', 'Espaço ocupado', 'Métrica', 'Tempo', 'Melhor iteração', 'Solução'])

arquivo_csv.writerow([f'instancias/basico/', 'N', 0, 1])
arquivo_csv.writerow([f'instancias/basico/', 'S', 30, 1])

for j in range(11):
    arquivo_csv.writerow([f'instancias/Multiconflito/multiconflito_{lista_instancia_multiconflito[0]}/', 'N', 0, str(j + 1)])

for instancia in lista_instancia_multiconflito:
    for j in range(11):
        arquivo_csv.writerow([f'instancias/Multiconflito/multiconflito_{instancia}/', 'S', instancia, str(j + 1)])

for instancia in lista_instancia:
    for i in range(5):
        indice = str(i).zfill(2)
        for j in range(11):
            arquivo_csv.writerow([f'instancias/{instancia}{indice}/', 'N', 0, str(j + 1)])
        for j in range(11):
            arquivo_csv.writerow([f'instancias/{instancia}{indice}/', 'S', 30, str(j + 1)])

arquivo.close()
