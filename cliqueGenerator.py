import random

def crearArcos(lista_adyacencias, nodoOrigen, nodoFinal):
    if nodoOrigen in lista_adyacencias and nodoFinal not in lista_adyacencias[nodoOrigen]:
            lista_adyacencias[nodoOrigen].append(nodoFinal)

def crearNodo(lista_adyacencias, nodo):
    if nodo not in lista_adyacencias:
        lista_adyacencias[nodo] = []

def generar_grafo(n, k):
    lista_adyacencias = {}
    nodes = list(range(1, n+1))
    for i in range(1, n+1):
        crearNodo(lista_adyacencias, i)

    clique_nodes = random.sample(nodes, k)
    for i in range(k):
        for j in range(i + 1, k):
            crearArcos(lista_adyacencias, clique_nodes[i], clique_nodes[j])
            crearArcos(lista_adyacencias, clique_nodes[j], clique_nodes[i])

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.1:
                crearArcos(lista_adyacencias, i, j)
                crearArcos(lista_adyacencias, j, i)
    return lista_adyacencias, clique_nodes

n = 100
k = 20
lista_adyacencias, clique_nodes = generar_grafo(n, k)
print(f"Grafo: {lista_adyacencias}")
print(f"Clique máximo real: {clique_nodes}")