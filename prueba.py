import random
import matplotlib.pyplot as plt
from pyeasyga import pyeasyga

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

#print(generar_grafo(10, 3))


def fitness(individual, graph):
    nodes_in_clique = [node for node, bit in enumerate(individual, start=1) if bit == 1]
    #print(nodes_in_clique)
    for i in nodes_in_clique:
        for j in nodes_in_clique:
            if i != j and (j not in graph[i] and i not in graph[j]):
                #return -len(nodes_in_clique)  # Penalización
                return 0
    return len(nodes_in_clique)


def create_individual(data):
    solucion = [0] * len(data)
    vertice_inicial = random.choice(range(n))
    solucion[vertice_inicial] = 1
    clique_actual = {vertice_inicial}
    #print("asdada",data)
    for v in range(n):
        if v not in clique_actual:
            if all((v, u) in data or (u, v) in data for u in clique_actual):
                solucion[v] = 1
                clique_actual.add(v)
    
    return solucion
    #return [random.randint(0, 1) for _ in range(len(data))]

def crossover(parent_1, parent_2):
    point = random.randint(1, len(parent_1) - 1)
    child_1 = parent_1[:point] + parent_2[point:]
    child_2 = parent_2[:point] + parent_1[point:]
    return child_1, child_2


def mutate(individual):
    index = random.randint(0, len(individual) - 1)
    individual[index] = 1 - individual[index]


def run_ga_and_collect_data(lista_adyacencias, population_size, elitism):
    ga = pyeasyga.GeneticAlgorithm(
        list(lista_adyacencias.keys()),
        population_size=population_size,
        generations=100,
        crossover_probability=0.8,
        mutation_probability=0.2,
        elitism=elitism,
        maximise_fitness=True
    )
    ga.create_individual = create_individual
    ga.crossover_function = crossover
    ga.mutate_function = mutate
    ga.fitness_function = lambda ind, _: fitness(ind, lista_adyacencias)
    
    avg_fitness_history = []
    best_fitness_history = []
    ga.create_first_generation()
    #print(ga.current_generation)
    
    for _ in range(100):
        fitness_po = [ind.fitness for ind in ga.current_generation]
        average = sum(fitness_po)/len(fitness_po)
        avg_fitness_history.append(average)
        best_fitness_history.append(ga.best_individual()[0]) #fitness del mejor individuo
        #print(ga.best_individual())
        ga.create_next_generation()
    
    print(avg_fitness_history)
    
    return avg_fitness_history, best_fitness_history

def plot_clique_fitness(lista_adyacencias, population_sizes, elitism):
    avg_history, best_history = run_ga_and_collect_data(lista_adyacencias, population_sizes, elitism)
    
    plt.figure()
    plt.plot(range(100), avg_history, label='Average Fitness')
    plt.plot(range(100), best_history, label='Best Fitness')
    plt.title(f'Population: {population_sizes}, Elitism: {elitism}')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()

n = 100
k = 20
lista_adyacencias, clique_nodes = generar_grafo(n, k)
print(f"Grafo: {lista_adyacencias}")
print(f"Clique máximo real: {clique_nodes}")


plot_clique_fitness(lista_adyacencias, 100, elitism=True)
