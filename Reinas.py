import random
from pyeasyga import pyeasyga


# Inicialice su representacion
# 1. No se pueden repetir números en la representación?, pq?
# 2. Que tengo que hacer si quiero un tablero mas grande?
#representacion = [0, 1, 2, 3, 4, 5, 6, 7]

def representacion (n):
    ret = []
    while len(ret) < n:
        k = random.randint(0,n-1)
        if k not in ret:
            ret.append(k)
    return ret

representacion = (representacion(12))

# Vamos a utilizar la librería pyeasyga que se encarga de los procesos de iteración del algoritmo. Creamos una instancia de la clase.
ga = pyeasyga.GeneticAlgorithm(representacion,
                            population_size=50,
                            generations=100,
                            crossover_probability=0.8,
                            mutation_probability=0.2,
                            elitism=True,
                            maximise_fitness=False)

def print_board(board_representation):
    def print_x_in_row(row_length, x_position):
        print('', end = '')
        for _ in range(row_length):
            print('---', end = '')
        print('\n|', end = '')
        for i in range(row_length):
            if i == x_position:
                print('{} |'.format('X'), end = '')
            else:
                print('  |', end = '')
        print('')

    def print_board_bottom(row_length):
        print('', end = '')
        for _ in range(row_length):
            print('---', end = '')

    num_of_rows = len(board_representation)
    row_length = num_of_rows    #rows == columns in a chessboard

    for row in range(num_of_rows):
        print_x_in_row(row_length, board_representation[row])

    print_board_bottom(row_length)
    print('\n', end = '')
    
def create_individual(data):
    individual = data[:]
    random.shuffle(individual)
    return individual

#Ejemplos de dos individuos que siguen nuestra representación
ind1eje = create_individual(representacion)
ind2eje = create_individual(representacion)

#print(ind1eje)
#print(ind2eje)

#Una vez la creamos la asignamos a nuestra instancia de ga.
ga.create_individual = create_individual


# Ahora definimos nuestra función de crossover
def crossover(parent_1, parent_2):
    crossover_index = random.randrange(1, len(parent_1))
    child_1a = parent_1[:crossover_index]
    child_1b = [i for i in parent_2 if i not in child_1a]
    child_1 = child_1a + child_1b

    child_2a = parent_2[crossover_index:]
    child_2b = [i for i in parent_1 if i not in child_2a]
    child_2 = child_2a + child_2b

    return child_1, child_2

#Ejemplo de operador de crossover
#print(crossover(ind1eje,ind2eje))


#Una vez la creamos la asignamos a nuestra instancia ga.
ga.crossover_function = crossover

#Definimos la función de mutación
def mutate(individual):
    mutate_index1 = random.randrange(len(individual))
    mutate_index2 = random.randrange(len(individual))
    individual[mutate_index1], individual[mutate_index2] = individual[mutate_index2], individual[mutate_index1]

#print(ind1eje)
mutate(ind1eje)
#print(ind1eje)

#Una vez la creamos la asignamos a nuestra instancia ga.
ga.mutate_function = mutate

# Función de selección!!, población es un objeto que contiene los individuos y sus atributos como la función de fitness
def selection(population):
    ## En el taller ustedes deben implementar una selección mas inteligente (ruleta)
    return random.choice(population)

#Una vez la creamos la asignamos a nuestra instancia ga.
ga.selection_function = selection


# Función de fitness: probablemente la mas importante
def fitness (individual, data):
    collisions = 0
    for item in individual:
        item_index = individual.index(item)
        for elem in individual:
            elem_index = individual.index(elem)
            if item_index != elem_index:
                if item - (elem_index - item_index) == elem or (elem_index - item_index) + item == elem:
                    collisions += 1
    return collisions

# Ejemplo cuantas colisiones tiene este individuo?
#coli = [0, 5, 3, 6, 7, 4, 1, 2]
#print_board(coli)#Para imprimir el board deben ejecutar primero la función al final del script
#print(fitness(coli,representacion))

#Una vez la creamos la asignamos a nuestra instancia ga.
ga.fitness_function = fitness       # set the GA's fitness function

#Primera generación
ga.create_first_generation()
print(ga.current_generation[0:10])


def datos_generacion():
    fitness_po = [i.fitness for i in ga.current_generation]
    average = sum(fitness_po)/len(fitness_po)
    print("Fitness promedio:{} ".format(average))
    print("Mejor Individuo: {}".format(ga.best_individual()))

datos_generacion()

# Para mostrar el tablero de cada individuo después de cada generación
def mostrar_tablero_generacion():
    # Imprime el mejor individuo de cada generación
    mejor_individuo = ga.best_individual()[0]  # Accedemos al primer elemento, que es el individuo
    print("Tablero de la mejor solución en esta generación:")
    print_board(mejor_individuo)  # Imprime el tablero con la representación del individuo
    print("--------------------------------------------------------")

# Para mostrar el tablero en las primeras generaciones
for i in range(1, 10):
    print("Generación #{}".format(i))
    ga.create_next_generation()
    datos_generacion()
    mostrar_tablero_generacion()  # Imprime el tablero del mejor individuo

    
#Para correr todas las generaciones definidas en la inicialización de ga.
ga.run()
ga.best_individual()