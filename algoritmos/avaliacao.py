from aproximativos import christofides, twice
from primitivas import geraGrafo
import time
from memory_profiler import memory_usage
from functools import partial
from multiprocessing import freeze_support
import signal
import os

def main():
	testaTodos = False
	numTestes = 1
	arquivoTestes = '../lista-datasets.txt'
	arquivoSaida = '../saida.csv'

	with open(arquivoTestes, 'r') as arquivo:
		linhas = arquivo.readlines()

	linhas = linhas[1:] # Remove a primeira linha (cabeçalho)

	if not os.path.exists(arquivoSaida):
		with open(arquivoSaida, 'w') as saida: # abre o arquivo de saida (se nao existir, cria)
			saida.write('Arquivo;Algoritmo;Tempo;Custo;Aproximacao;Memoria\n')

	if testaTodos:
		numTestes = len(linhas)

	for linha in linhas[:numTestes]:
		
		linha = linha.split() # arquivo, dimensao, custo otimo
		arquivo = '../datasets/' + linha[0] + '.tsp'

		try:
			grafo = geraGrafo(arquivo)
		except:
			print('Erro em geraGrafo: Arquivo nao encontrado')
			continue

		with open(arquivoSaida, 'a') as saida:
			saida.write(linha[0] + ';')
			saida.write('Christofides;')

		# inicia o teste com Christofides
		def timeout_handler(signum, frame):
			raise TimeoutError(f'Erro: Tempo limite excedido para o dataset {linha[0]}')

		signal.signal(signal.SIGALRM, timeout_handler)
		signal.alarm(30*60)

		inicioCristo = time.time()
		try:
			custoCristo = christofides(grafo)
		except TimeoutError:
			print(f'Erro: Tempo limite excedido para o christofides do dataset {linha[0]}')

		fimCristo = time.time()

		signal.alarm(0)

		memoria = memory_usage(partial(christofides, grafo), interval=1.0, max_usage=True)
		
		with open(arquivoSaida, 'a') as saida:
			saida.write('{};'.format(round(fimCristo-inicioCristo, 5))) # tempo
			saida.write('{};'.format(round(custoCristo, 2))) # custo
			saida.write('{};'.format(round(custoCristo/float(linha[2]), 2))) # aproximacao
			saida.write('{}'.format(round(memoria, 2))) # memoria
			saida.write('\n')

			saida.write(linha[0] + ';')
			saida.write('Twice around the tree;')	

		signal.signal(signal.SIGALRM, timeout_handler)
		signal.alarm(30*60)
		
		# inicia o teste com Twice around the tree
		inicioTwice = time.time()
		try:
			custoTwice = twice(grafo)
		except TimeoutError:
			print(f'Erro: Tempo limite excedido para o twice do dataset {linha[0]}')

		fimTwice = time.time()
		
		signal.alarm(0)

		memoria = memory_usage(partial(twice, grafo), interval=1.0, max_usage=True)
		
		with open(arquivoSaida, 'a') as saida:
			saida.write('{};'.format(round(fimTwice-inicioTwice, 5))) # tempo
			saida.write('{};'.format(round(custoTwice, 2))) # custo
			saida.write('{};'.format(round(custoTwice/float(linha[2]), 2))) # aproximacao
			saida.write('{}'.format(round(memoria, 2))) # memoria
			saida.write(';\n')

if __name__ == '__main__':
	freeze_support()
	main()
	