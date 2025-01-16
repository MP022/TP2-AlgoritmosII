# Padrão: Anaconda 22.9 e/ou Python +3.9 com NumPy, SciPy e Pandas.
# Bibliotecas: Networkx, iGraph.

import os
from math import *
import pandas
from networkx import *
from timeout_decorator import timeout
import time

## Preicsa implementar: ##
# algoritmo branch-and-bound, 
# algoritmo twice-around-the-tree, 
# algoritmo de Christofides 
## para solucionar o problema do caixeiro viajante geométrico. ##

# deverão avaliar o desempenho dos algoritmos segundo três aspectos: tempo, espaço, e qualidade da solução.
# tempo de processamento deve ser limitado a 30min. dados referentes à execução colocados como NA (não-disponível).

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

@timeout(seconds=1800)
def TSP_branch_and_Bound(grafo: Graph):
    # TODO: ALTERAR A ESTIMATIVA PRA TIRAR AS COPIAS DE GRAFOS E DIMINUIR O PROCESSAMENTOS DE __len__ OU QUALQUER OUTRA COISA QUE DER
    def estimativa(grafoEst: Graph, caminho: list) -> int:
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

            if u in caminho and caminho.__len__() > 1:
                ind: int = caminho.index(u)
                if ind == 0:
                    menor2 = grafoEst.get_edge_data(u,caminho[ind+1])['weight']
                elif ind == caminho.__len__()-1:
                    menor2 = grafoEst.get_edge_data(u,caminho[ind-1])['weight']
                else:
                    menor1 = grafoEst.get_edge_data(u,caminho[ind-1])['weight']
                    menor2 = grafoEst.get_edge_data(u,caminho[ind+1])['weight']
            est += menor1 + menor2
            menor1 = 0
            menor2 = 0
        return est/2

    quantN = grafo.number_of_nodes()

    # custo total das arestas
    custoTotal: int = 0
    for u in range(0, grafo.number_of_nodes()):
        for v in grafo.neighbors(u):
            custoTotal += grafo.get_edge_data(u,v)['weight']
    custoTotal = custoTotal/2

    no = {'estimativa': estimativa(grafo, [0]), 'profundidade': 1, 'custo': 0, 'caminho': [0]}
    fila = [no]
    melhorCusto = custoTotal+1
    caminho = []
    
    while fila.__len__() > 0:
        no = fila.__getitem__(0)
        fila.remove(no)
        noAtual = no['caminho'][-1]

        if no['profundidade'] > quantN and melhorCusto > no['custo']:

            melhorCusto = no['custo']
            caminho = no['caminho']

        elif no['estimativa'] < melhorCusto:

            if no['profundidade'] < quantN:

                for k in range(1, quantN):

                    if not(k in no['caminho']):
                        no['caminho'].append(k)
                        est = estimativa(grafo, no['caminho'])
                    else:
                        continue

                    if grafo[noAtual][k] != custoTotal+1 and est < melhorCusto:

                        item = {'estimativa': est, 'profundidade': no['profundidade']+1, 'custo': no['custo'] + grafo[noAtual][k]['weight'], 'caminho': no['caminho'].copy()}
                        insere_decres_list(fila, item, 'estimativa')

                    no['caminho'].remove(k)

            elif noAtual != 0 and grafo[0][noAtual] != custoTotal+1 and no['custo']+grafo[noAtual][0]['weight'] < melhorCusto and (set(grafo.nodes) & set(no['caminho'])) == set(grafo.nodes):
                
                no['caminho'].append(0)
                item = {'estimativa': no['custo']+grafo[noAtual][0]['weight'], 'profundidade': no['profundidade']+1, 'custo': no['custo'] + grafo[noAtual][0]['weight'], 'caminho': no['caminho']}
                insere_decres_list(fila, item, 'estimativa')

    return melhorCusto
 
@timeout(seconds=1800)
def TSP_twice_around_the_tree(grafo: Graph):
    arvore: Graph = minimum_spanning_tree(grafo, algorithm="prim")
    
    dfs: list = list(dfs_preorder_nodes(arvore))
    
    hamilton = []
    for n in dfs:
        if not(n in hamilton):
            hamilton.append(n)
    hamilton.append(hamilton[0])

    melhorCusto = 0
    for i in range(0, hamilton.__len__()-1):
        melhorCusto += grafo[hamilton[i]][hamilton[i+1]]['weight']

    return melhorCusto

@timeout(seconds=1800)
def TSP_christofides(grafo: Graph):

    def no_grau_impar(no: dict):
        return arvore.degree()[no] % 2 == 1

    arvore: Graph = minimum_spanning_tree(grafo, algorithm="prim")
    I: Graph = Graph()

    nosImpares = []
    for n in filter(no_grau_impar, arvore):
        nosImpares.append(n)

    # print(arvore.degree)
    # print(nosImpares)

    I.add_nodes_from(nosImpares)

    for u in nosImpares:
        for v in grafo.neighbors(u):
            if v in nosImpares:
                I.add_edges_from([(u, v)])
                I[u][v]['weight'] = dist(grafo.nodes[u]['coord'], grafo.nodes[v]['coord'])

    match = list(min_weight_matching(I))
    # print(match)
    for aresta in range(0, match.__len__()):
        u, v = match[aresta]
        match[aresta] = (u, v, {'weight': grafo[u][v]['weight']})
    
    gLinha = MultiGraph(arvore)
    gLinha.add_edges_from(match)
    sol = []
    for n in eulerian_circuit(gLinha):
        if not(n[0] in sol):
            sol.append(n[0])
    sol.append(sol[0])

    melhorCusto = 0
    for i in range(0, sol.__len__()-1):
        melhorCusto += grafo[sol[i]][sol[i+1]]['weight']

    return melhorCusto

def executa_teste(arquivo):
    # abre o arquivo
    infile = open(arquivo, 'r')

    # le o cabeçalho
    dimension = 8000
    linha = infile.readline().strip()
    nomeArqSaida = linha.split()[-1]
    while not linha.__contains__('NODE'):
        print(linha)
        linha = infile.readline().strip()
        if linha.split()[0].__contains__('DIMENSION'):
            dimension = linha.split()[-1]

    if int(dimension) > 7000:
        print("\n\nMEU COMPUTADOR NÂO RODA\n\n")
        infile.close()
        return

    #  le a lista de nos
    nos = []
    linha = infile.readline().strip().split()
    while linha != [] and linha[0] != 'EOF':
        nos.append((nos.__len__(), {'coord': (float(linha[-2]), float(linha[-1]))}))
        linha = infile.readline().strip().split()

    # fecha o arquivo
    infile.close()

    grafoTeste = Graph()
    grafoTeste.add_nodes_from(nos)

    arestas = []
    for u in range(0, nos.__len__()):
        for v in range(u+1, nos.__len__()):
            arestas.append((u, v, dist(grafoTeste.nodes[u]['coord'], grafoTeste.nodes[v]['coord'])))

    grafoTeste.add_weighted_edges_from(arestas)

    tempoDeExecução = time.time()
    try:
        branchAndBound = TSP_branch_and_Bound(grafoTeste)
    except:
        branchAndBound = 'NA'
    branchAndBound = 'Branch and bound:\nSolução: ' + str(branchAndBound) + '\nTempo: ' + str(time.time() - tempoDeExecução) + '\n\n'
    print(branchAndBound)

    tempoDeExecução = time.time()
    try:
        twiceAroundTheTree = TSP_twice_around_the_tree(grafoTeste)
    except:
        twiceAroundTheTree = 'NA'
    twiceAroundTheTree = 'Twice around the tree:\nSolução: ' + str(twiceAroundTheTree) + '\nTempo: ' + str(time.time() - tempoDeExecução) + '\n\n'
    print(twiceAroundTheTree)

    tempoDeExecução = time.time()
    try:
        christofides = TSP_christofides(grafoTeste)
    except:
        christofides = 'NA'
    christofides = 'Christofides:\nSolução: ' + str(christofides) + '\nTempo: ' + str(time.time() - tempoDeExecução) + '\n'
    print(christofides)
    


    infile = open('./resultados/'+nomeArqSaida+'.txt', 'w')

    infile.write(nomeArqSaida + ' -- ' + dimension + '\n\n' + branchAndBound + twiceAroundTheTree + christofides)

    infile.close()

def gera_resultados_por_algoritmo():
    try:
        arquivosResultados.remove('branchAndBound.txt')
    except:
        not True
    try:
        arquivosResultados.remove('twiceAroundTheTree.txt')
    except:
        not True
    try:
        arquivosResultados.remove('christofides.txt')
    except:
        not True

    branchAndBound = ''
    twiceAroundTheTree = ''
    christofides = ''
    for i in arquivosResultados:
        infile = open('./resultados/' + i, 'r')
        linha = infile.readline().strip()
        branchAndBound += linha + "\n"
        twiceAroundTheTree += linha + "\n"
        christofides += linha + "\n"
        infile.readline().strip()
        infile.readline().strip()
        linha = infile.readline().strip()
        branchAndBound += linha + "\n"
        linha = infile.readline().strip()
        branchAndBound += linha + "\n\n"
        infile.readline().strip()
        infile.readline().strip()
        linha = infile.readline().strip()
        twiceAroundTheTree += linha + "\n"
        linha = infile.readline().strip()
        twiceAroundTheTree += linha + "\n\n"
        infile.readline().strip()
        infile.readline().strip()
        linha = infile.readline().strip()
        christofides += linha + "\n"
        linha = infile.readline().strip()
        christofides += linha + "\n\n"


    infile = open('./resultados/branchAndBound.txt', 'w')

    infile.write(branchAndBound)

    infile.close()

    infile = open('./resultados/twiceAroundTheTree.txt', 'w')

    infile.write(twiceAroundTheTree)

    infile.close()

    infile = open('./resultados/christofides.txt', 'w')

    infile.write(christofides)

    infile.close()

arquivosTeste = os.listdir('./teste/')
arquivosTeste.sort()

# Retira teste que já foram executados
arquivosResultados = os.listdir('./resultados/')
for i in arquivosResultados:
    if (i.split('.')[0]+'.tsp') in arquivosTeste: arquivosTeste.remove(i.split('.')[0]+'.tsp')

for i in arquivosTeste:
    executa_teste('./teste/'+i)

gera_resultados_por_algoritmo()

# TODO: Gera graficos a partir dos dados de teste
arquivosResultados = os.listdir('./a/')
if not('branchAndBound.txt' in arquivosResultados) or not('twiceAroundTheTree.txt' in arquivosResultados) or not('christofides.txt' in arquivosResultados):
    print("Resultados por algoritmos não foram gerados.")
    exit()

infile = open('./a/branchAndBound.txt', 'r')
branchAndBoundFile = infile.readlines()
infile.close()
infile = open('./a/twiceAroundTheTree.txt', 'r')
twiceAroundTheTreeFile = infile.readlines()
infile.close()
infile = open('./a/christofides.txt', 'r')
christofidesFile = infile.readlines()
infile.close()

branchAndBoundDictTempo = {}
for n in range(0, int(branchAndBoundFile.__len__()/4)):
    branchAndBoundDictTempo[branchAndBoundFile[n*4][:-4]] = float(branchAndBoundFile[(n*4)+2].split(' ')[1][:-1])

twiceAroundTheTreeDictTempo = {}
for n in range(0, int(twiceAroundTheTreeFile.__len__()/4)):
    twiceAroundTheTreeDictTempo[twiceAroundTheTreeFile[n*4][:-4]] = float(twiceAroundTheTreeFile[(n*4)+2].split(' ')[1][:-1])

christofidesDictTempo = {}
for n in range(0, int(christofidesFile.__len__()/4)):
    christofidesDictTempo[christofidesFile[n*4][:-4]] = float(christofidesFile[(n*4)+2].split(' ')[1][:-1])

# print(branchAndBoundDictTempo)
# print(twiceAroundTheTreeDictTempo)
# print(christofidesDictTempo)

df = pandas.DataFrame({"twiceAroundTheTree": twiceAroundTheTreeDictTempo, "christofides": christofidesDictTempo})

fig = df.plot(kind='line', figsize=(5, 3), fontsize=5).get_figure()
fig.savefig('./a/test.pdf')

