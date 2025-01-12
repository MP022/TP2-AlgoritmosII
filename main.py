# Padrão: Anaconda 22.9 e/ou Python +3.9 com NumPy, SciPy e Pandas.
# Bibliotecas: Networkx, iGraph.

from math import *
import numpy
import scipy
import pandas
from networkx import *
import igraph

## Preicsa implementar: ##
# algoritmo branch-and-bound, 
# algoritmo twice-around-the-tree, 
# algoritmo de Christofides 
## para solucionar o problema do caixeiro viajante geométrico. ##

# deverão avaliar o desempenho dos algoritmos segundo três aspectos: tempo, espaço, e qualidade da solução.
# tempo de processamento deve ser limitado a 30min. dados referentes à execução colocados como NA (não-disponível).

# Declara um grafo completo com numNodes nós e os campos que serão usados nos algoritmos
def TSP_grafo_completo_vazio(numNodes: int) -> Graph:
    grafoVazio: Graph = complete_graph(numNodes)
    for n in range(0, grafoVazio.number_of_nodes()):
        grafoVazio.nodes[n]['coord'] = (0,0)

    for u in range(0, grafoVazio.number_of_nodes()):
        for v in range(u+1, grafoVazio.number_of_nodes()):
            grafoVazio.edges[u, v]['weight'] = 1
    
    return grafoVazio

def custo_total(grafo) -> int:
    soma: int = 0
    for u in range(0, grafo.number_of_nodes()):
        for v in grafo.neighbors(u):
            soma += grafo.get_edge_data(u,v)['weight']
    return soma/2

def dist(a: tuple, b: tuple) -> int:
    return sqrt((b[0]-a[0])*(b[0]-a[0])+(b[1]-a[1])*(b[1]-a[1]))

def insere_decres_list(list: list[dict[str, any]], item: any, valOrdem: str):
        n = list.__len__()
        iMax = n - 1
        iMin = 0

        # caso lista vazia
        if iMax - iMin == -1:
            list.insert(0, item)
            return

        while iMax - iMin > 1:
            if list[floor((iMax-iMin)/2)+iMin][valOrdem] > item[valOrdem]:
                iMax = floor((iMax-iMin)/2)+iMin
            else:
                iMin = floor((iMax-iMin)/2)+iMin

        # caso lista com 1 item
        if iMax - iMin < 1:
            if list[iMin][valOrdem] < item[valOrdem]:
                list.insert(1, item)
            else:
                list.insert(0, item)
            return

        # caso lista com mais de 1 item
        if list[iMax][valOrdem] < item[valOrdem]:
            list.insert(iMax + 1, item)
        elif list[iMin][valOrdem] < item[valOrdem]:
            list.insert(iMin + 1, item)
        else:
            list.insert(iMin, item)
        return

def TSP_branch_and_Bound(grafo: Graph):
    # TODO: ALTERAR A ESTIMATIVA PRA TIRAR AS COPIAS DE GRAFOS E DIMINUIR O PROCESSAMENTOS DE __len__ OU QUALQUER OUTRA COISA QUE DER
    
    # custo total das arestas
    custoTotal = custo_total(grafo)

    def estimativa(grafoEst: Graph) -> int:
        est: int = 0
        menor1 = menor2 = 0
        for u in grafoEst.nodes:
            for v in grafoEst.neighbors(u):
                aux = grafoEst.get_edge_data(u,v)['weight']
                if(aux < menor1 or menor1 == 0):
                    if (menor1 < menor2 or menor2 == 0):
                        menor2 = menor1
                    menor1 = aux
                    continue

                if(aux < menor2 or menor2 == 0):
                    menor2 = aux
                    continue
            est += menor1 + menor2
            menor1 = 0
            menor2 = 0
        return est/2

    quantN = grafo.number_of_nodes()

    # (estimativa, custoAtual, caminhoAteAqui)
    no = {'estimativa': estimativa(grafo), 'profundidade': 1, 'custo': 0, 'caminho': [0]}
    fila = [no]
    melhorCusto = custoTotal+1
    caminho = []
    
    while fila.__len__() > 0:
        no = fila.__getitem__(0)
        fila.remove(no)
        noAtual = no['caminho'][-1]
        print(noAtual, fila.__len__())

        # Remove todas as arestas já consideradas na solução.
        # grafoAux = Graph(grafo)
        # for i in range(1, no['caminho'].__len__()-1):
        #     grafoAux.remove_node(i)

        if no['profundidade'] > quantN and melhorCusto > no['custo']:

            melhorCusto = no['custo']
            caminho = no['caminho']

        elif no['estimativa'] < melhorCusto:

            if no['profundidade'] < quantN:

                est = estimativa(grafo) + no['custo']

                for k in range(1, quantN):

                    if not(k in no['caminho']) and grafo[noAtual][k] != custoTotal+1 and est < melhorCusto:

                        no['caminho'].append(k)
                        item = {'estimativa': est, 'profundidade': no['profundidade']+1, 'custo': no['custo'] + grafo[noAtual][k]['weight'], 'caminho': no['caminho'].copy()}
                        no['caminho'].remove(k)
                        insere_decres_list(fila, item, 'estimativa')

            elif noAtual != 0 and grafo[0][noAtual] != custoTotal+1 and no['custo']+grafo[noAtual][0]['weight'] < melhorCusto and (set(grafo.nodes) & set(no['caminho'])) == set(grafo.nodes):
                
                no['caminho'].append(0)
                item = {'estimativa': no['custo']+grafo[noAtual][0]['weight'], 'profundidade': no['profundidade']+1, 'custo': no['custo'] + grafo[noAtual][0]['weight'], 'caminho': no['caminho']}
                insere_decres_list(fila, item, 'estimativa')

    return (caminho, melhorCusto)
 
def TSP_twice_around_the_tree():
    print("TSP_twice_around_the_tree não implementado")
    return

def TSP_christofides():
    print("TSP_christofides não implementado")
    return

# nos = [(0, {'coord': (41,49)}), (1, {'coord': (35,17)}), (2, {'coord': (55,45)}), (3, {'coord': (55,20)}), (4, {'coord': (15,30)})]
# grafoTeste = Graph()
# grafoTeste.add_nodes_from(nos)
# arestas = [(0, 1, dist(grafoTeste.nodes[0]['coord'], grafoTeste.nodes[1]['coord'])), (0, 2, dist(grafoTeste.nodes[0]['coord'], grafoTeste.nodes[2]['coord'])), (0, 3, dist(grafoTeste.nodes[0]['coord'], grafoTeste.nodes[3]['coord'])), (0, 4, dist(grafoTeste.nodes[0]['coord'], grafoTeste.nodes[4]['coord'])),
#            (1, 2, dist(grafoTeste.nodes[1]['coord'], grafoTeste.nodes[2]['coord'])), (1, 3, dist(grafoTeste.nodes[1]['coord'], grafoTeste.nodes[3]['coord'])), (1, 4, dist(grafoTeste.nodes[1]['coord'], grafoTeste.nodes[4]['coord'])),
#            (2, 3, dist(grafoTeste.nodes[2]['coord'], grafoTeste.nodes[3]['coord'])), (2, 4, dist(grafoTeste.nodes[2]['coord'], grafoTeste.nodes[4]['coord'])),
#            (3, 4, dist(grafoTeste.nodes[3]['coord'], grafoTeste.nodes[4]['coord']))]
# grafoTeste.add_weighted_edges_from(arestas)

# nos = [0, 1, 2, 3, 4]
# arestas = [(0, 1, 3), (0, 2, 1), (0, 3, 5), (0, 4, 8),
#            (1, 2, 5), (1, 3, 7), (1, 4, 9),
#            (2, 3, 4), (2, 4, 2),
#            (3, 4, 3)]
# grafoTeste = Graph()
# grafoTeste.add_nodes_from(nos)
# grafoTeste.add_weighted_edges_from(arestas)

# grafoTeste = TSP_grafo_completo_vazio(100)

# abre o arquivo
# infile = open('./teste/berlin52.tsp', 'r')
infile = open('./teste/eil51.tsp', 'r')

# le o cabeçalho
linha = infile.readline().strip()
while not linha.__contains__('NODE'):
    print(linha)
    linha = infile.readline().strip()

#  le a lista de nos
nos = []
linha = infile.readline().strip()
while linha != 'EOF':
    x,y = linha.split()[1:]
    nos.append((nos.__len__(), {'coord': (float(x), float(y))}))
    linha = infile.readline().strip()

# fecha o arquivo
infile.close()

grafoTeste = Graph()
grafoTeste.add_nodes_from(nos)

arestas = []
for u in range(0, nos.__len__()):
    for v in range(u+1, nos.__len__()):
        arestas.append((u, v, dist(grafoTeste.nodes[u]['coord'], grafoTeste.nodes[v]['coord'])))

grafoTeste.add_weighted_edges_from(arestas)

# print(grafoTeste)
# print(grafoTeste.nodes)
# print(grafoTeste.edges)
print(TSP_branch_and_Bound(grafoTeste))
