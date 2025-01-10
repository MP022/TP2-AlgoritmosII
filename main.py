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
            grafoVazio.edges[u, v]['weight'] = 0
    
    return grafoVazio

def TSP_branch_and_Bound(grafo: Graph):
    print("TSP_branch_and_Bound não implementado")
    return

def TSP_twice_around_the_tree():
    print("TSP_twice_around_the_tree não implementado")
    return

def TSP_christofides():
    print("TSP_christofides não implementado")
    return

grafoTeste = TSP_grafo_completo_vazio(10000)
print(grafoTeste)
