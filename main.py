import os
import time
import pandas
from math import *
from networkx import *
import matplotlib.pyplot as plt
from timeout_decorator import timeout

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

    I.add_nodes_from(nosImpares)

    for u in nosImpares:
        for v in grafo.neighbors(u):
            if v in nosImpares:
                I.add_edges_from([(u, v)])
                I[u][v]['weight'] = dist(grafo.nodes[u]['coord'], grafo.nodes[v]['coord'])

    match = list(min_weight_matching(I))
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

def executa_teste(arquivo: str):
    # abre o arquivo
    infile = open(arquivo, 'r')

    # le o cabeçalho
    dimension = 7001
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
    try:
        arquivosResultados.remove('melhoresResultados.txt')
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

arquivosResultados = os.listdir('./resultados/')
if not('branchAndBound.txt' in arquivosResultados) or not('twiceAroundTheTree.txt' in arquivosResultados) or not('christofides.txt' in arquivosResultados):
    print("Resultados por algoritmos não foram gerados.")
    exit()

infile = open('./resultados/branchAndBound.txt', 'r')
branchAndBoundFile = infile.readlines()
infile.close()
infile = open('./resultados/twiceAroundTheTree.txt', 'r')
twiceAroundTheTreeFile = infile.readlines()
infile.close()
infile = open('./resultados/christofides.txt', 'r')
christofidesFile = infile.readlines()
infile.close()

branchAndBoundDictTempo = {}
for n in range(0, int(branchAndBoundFile.__len__()/4)):
    branchAndBoundDictTempo[int(branchAndBoundFile[n*4].split(' ')[-1][:-1])] = float(branchAndBoundFile[(n*4)+2].split(' ')[1][:-1])

twiceAroundTheTreeDictResultado = {}
for n in range(0, int(twiceAroundTheTreeFile.__len__()/4)):
    twiceAroundTheTreeDictResultado[int(twiceAroundTheTreeFile[n*4].split(' ')[-1][:-1])] = float(twiceAroundTheTreeFile[(n*4)+2].split(' ')[1][:-1])

christofidesDictResultado = {}
for n in range(0, int(christofidesFile.__len__()/4)):
    christofidesDictResultado[int(christofidesFile[n*4].split(' ')[-1][:-1])] = float(christofidesFile[(n*4)+2].split(' ')[1][:-1])

listaQuantCidades = {}
for n in range(0, int(branchAndBoundFile.__len__()/4)):
    listaQuantCidades[int(branchAndBoundFile[n*4].split(' ')[-1][:-1])] = branchAndBoundFile[n*4].split(' ')[0]
listaQuantCidades = dict(sorted(listaQuantCidades.items()))

df = pandas.DataFrame({"N° de cidades": listaQuantCidades, "Branch and Bound": branchAndBoundDictTempo, "Twice-around-the-tree": twiceAroundTheTreeDictResultado, "Christofides": christofidesDictResultado})

fig = df.plot(title="Resultados dos testes", x="N° de cidades", ylabel="N° de segundos", kind='line', figsize=(10, 7), color=['r', 'b', 'm'], marker = 'o').get_figure()
fig.savefig('./Figura1.pdf')

df = pandas.DataFrame({"N° de cidades": listaQuantCidades, "Twice-around-the-tree": twiceAroundTheTreeDictResultado})

fig = df.plot(title="Resultados dos testes no Twice-around-the-tree", x="N° de cidades", ylabel="N° de segundos", kind='line', figsize=(10, 7), color='b', marker = 'o').get_figure()
fig.savefig('./Figura2.pdf')

infile = open('./resultados/melhoresResultados.txt', 'r')
melhoresResultadosFile = infile.readlines()
infile.close()

melhoresResultadosDictResultado = {}
for n in range(0, int(melhoresResultadosFile.__len__())):
    melhoresResultadosDictResultado[melhoresResultadosFile[n].split(' ')[0]] = float(melhoresResultadosFile[n].split(' ')[-1][:-1])

twiceAroundTheTreeDictResultado = {}
for n in range(0, int(twiceAroundTheTreeFile.__len__()/4)):
    twiceAroundTheTreeDictResultado[twiceAroundTheTreeFile[n*4].split(' ')[0]] = float(twiceAroundTheTreeFile[(n*4)+1].split(' ')[1][:-1])

christofidesDictResultado = {}
for n in range(0, int(christofidesFile.__len__()/4)):
    if christofidesFile[(n*4)+1].split(' ')[1][:-1] != 'NA':
        christofidesDictResultado[christofidesFile[n*4].split(' ')[0]] = float(christofidesFile[(n*4)+1].split(' ')[1][:-1])
    else:
        christofidesDictResultado[christofidesFile[n*4].split(' ')[0]] = 0

listaNomeTeste = {}
for n in range(0, int(branchAndBoundFile.__len__()/4)):
    listaNomeTeste[int(branchAndBoundFile[n*4].split(' ')[-1][:-1])] = branchAndBoundFile[n*4].split(' ')[0]
listaNomeTeste = dict(sorted(listaNomeTeste.items()))
print(twiceAroundTheTreeDictResultado)

df = pandas.DataFrame({"Nome do teste": listaNomeTeste, "Melhor Resultado": melhoresResultadosDictResultado, "Twice-around-the-tree": twiceAroundTheTreeDictResultado, "Christofides": christofidesDictResultado})

fig = df.plot(title="Resultados dos testes", x="Nome do teste", ylabel="Distancia do resultado", kind='line', figsize=(10, 7), color=['r', 'b', 'm'], marker = 'o').get_figure()
fig.savefig('./Figura3.pdf')
