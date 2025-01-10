# Padrão: Anaconda 22.9 e/ou Python +3.9 com NumPy, SciPy e Pandas.
# Bibliotecas: Networkx, iGraph.

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

def TSP_branch_and_Bound(grafo: Graph):
    def estimativa() -> int:
        est = 0
        menor1 = 0
        menor2 = 0
        for u in range(0, grafo.number_of_nodes()):
            vizinhos = grafo.neighbors(u)
            for v in vizinhos:
                aux = grafo.get_edge_data(u,v)['weight']
                if(aux < menor1 or menor1 == 0):
                    menor1 = aux
                    continue

                if(aux < menor2 or menor2 == 0):
                    menor2 = aux
                    continue
            est += menor1 + menor2
        return est/2
    
    est = estimativa()
    return

def TSP_twice_around_the_tree():
    print("TSP_twice_around_the_tree não implementado")
    return

def TSP_christofides():
    print("TSP_christofides não implementado")
    return

grafoTeste = TSP_grafo_completo_vazio(100)
TSP_branch_and_Bound(grafoTeste)
