import matplotlib.pyplot as plt
from pyeasyga import pyeasyga
import random
import numpy as np

def representacion_fun(n):
    ret = []
    while len(ret) < n:
        k = random.randint(0, n - 1)
        if k not in ret:
            ret.append(k)
    return ret

def create_individual(data):
    individual = data[:]
    random.shuffle(individual)
    return individual

def crossover(parent_1, parent_2):
    crossover_index = random.randrange(1, len(parent_1))
    child_1a = parent_1[:crossover_index]
    child_1b = [i for i in parent_2 if i not in child_1a]
    child_1 = child_1a + child_1b

    child_2a = parent_2[crossover_index:]
    child_2b = [i for i in parent_1 if i not in child_2a]
    child_2 = child_2a + child_2b

    return child_1, child_2

def mutate(individual):
    mutate_index1 = random.randrange(len(individual))
    mutate_index2 = random.randrange(len(individual))
    individual[mutate_index1], individual[mutate_index2] = individual[mutate_index2], individual[mutate_index1]

def fitness(individual, data):
    collisions = 0
    for item in individual:
        item_index = individual.index(item)
        for elem in individual:
            elem_index = individual.index(elem)
            if item_index != elem_index:
                if item - (elem_index - item_index) == elem or (elem_index - item_index) + item == elem:
                    collisions += 1
    return collisions

def selection(population):
    epsilon = 0.000000001  # Para manejar fitness de 0
    fitness_values = np.array([ind.fitness for ind in population])
    adjusted_fitness = 1 / (fitness_values + epsilon)
    probabilities = adjusted_fitness / adjusted_fitness.sum() #favorables/totales
    selected_index = np.random.choice(len(population), p=probabilities)
    return population[selected_index]

def selection2(population):
    ## En el taller ustedes deben implementar una selección mas inteligente (ruleta)
    return random.choice(population)

def run_ga_and_collect_data(representacion, population_size, elitism):
    ga = pyeasyga.GeneticAlgorithm(
        representacion,
        population_size=population_size,
        generations=100,
        crossover_probability=0.8,
        mutation_probability=0.2,
        elitism=elitism,
        maximise_fitness=False
    )

    ga.create_individual = create_individual
    ga.crossover_function = crossover
    ga.mutate_function = mutate
    ga.fitness_function = fitness
    ga.selection_function = selection

    average_fitness_history = []
    best_fitness_history = []
    ga.create_first_generation()
    

    for _ in range(100): #generaciones
        fitness_po = [ind.fitness for ind in ga.current_generation]
        average = sum(fitness_po)/len(fitness_po)
        average_fitness_history.append(average)
        best_fitness_history.append(ga.best_individual()[0]) #fitness del mejor individuo
        #print(ga.best_individual())
        ga.create_next_generation()

    return average_fitness_history, best_fitness_history

# Representacion inicial
n = 12
representacion = representacion_fun(n)

def plot_fitness_evolution(population_sizes, elitism):
    for population_size in population_sizes:
        avg_history, best_history = run_ga_and_collect_data(
            representacion, population_size, elitism
        )

        plt.figure()
        plt.plot(range(100), avg_history, label='Average Fitness')
        plt.plot(range(100), best_history, label='Mejor Individuo')
        plt.title(f'Tamaño poblacion: {population_size}, Elitismo: {elitism}')
        plt.xlabel('Generación')
        plt.ylabel('Fitness')
        plt.legend()
        plt.show()

plot_fitness_evolution([50], elitism=True) #A3.1

plot_fitness_evolution([10, 100, 200, 500], elitism=True) #A3.2

plot_fitness_evolution([50], elitism=False) #A3.3
