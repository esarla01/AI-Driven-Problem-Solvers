
from random import choices, random, randint, sample
from typing import List, Tuple
import itertools

# Assignment 4: The Knapsack Problem 
# Goal: Solve the knapsack problme using a genetic algorithm.


# -------------------------------------------------- Box Class -------------------------------------------------- #


# The box class represents each individual box with weight and importance values.
class Box: 
        def __init__(self, number : int, weight : int, importance: int):
            self.number = number
            self.weight = weight
            self.importance = importance
        
        def get_number(self):
            return self.number

        def get_weight(self):
            return self.weight
        
        def get_importance(self):
            return self.importance

# Each box given in the given version of the knapsack problem is added to a list named ListBoxes.
ListBoxes  = []
ListBoxes.append(Box(1, 20, 6))
ListBoxes.append(Box(2, 30, 5))
ListBoxes.append(Box(3, 60, 8))
ListBoxes.append(Box(4, 90, 7))
ListBoxes.append(Box(5, 50, 6))
ListBoxes.append(Box(6, 70, 9))
ListBoxes.append(Box(7, 30, 4))
ListBoxes.append(Box(8, 30, 5))
ListBoxes.append(Box(9, 70, 4))
ListBoxes.append(Box(10, 20, 9))
ListBoxes.append(Box(11, 20, 2))
ListBoxes.append(Box(12, 60, 1))


# -------------------------------------------------- Operations on a  Generation -------------------------------------------------- #


# Genome: is a possible solution to the problem. 
Genome = List[int]

# Population: is the pool of genomes that are created after a given iteration.
Population = List[Genome]

# Generates a new solution! Returns a list with each location having a value of 0 or 1. 
def generate_individual(length : int):
    # Value 0 and 1 at index i indicates whether the new solution includes the box at 
    # index i in the list of boxes. (0 implies it is included and 1 implies otherwise.)
    return choices([0, 1], k=length)  


# Generates a new population made up of randomly generated individuals!
def generate_population(size : int, length : int):

    random_population = []
    for x in range(size):
        random_population.append(generate_individual(length))

    return random_population


# Modifies the genomes of two individual after a random crossover occurs between them! 
def single_crossover(genome1 : Genome, genome2 : Genome):

    length = len(genome1)       
    point = randint(1, length - 1)  # Picks a random point on both genomes.

    # Splits both genomes into two pieces. Switchs the end piece of both.
    crossed_genome1 = genome1[0:point] + genome2[point:] 
    crossed_genome2 = genome2[0:point] + genome1[point:]

    return crossed_genome1, crossed_genome2  


# Modifies the genomes of two individual after a random crossover occurs between them! 
def mutation(genome : Genome, probability : float):

    if random() <= probability: # the probability of the mutation is evaluated
        index = randint(0, len(genome) - 1) # picks a random spot on the genome 
        genome[index] = abs(genome[index] - 1) # the spot becomes 0 if it was 1 ealier, vice versa

    return genome



# Calculates the fitness value of input genome based on the total weight and importance values
def fitness_function(genome : Genome):
    fitness_value = 0 
    total_weight = 0
    total_importance = 0   
    # sum weight and importance value of all the items in the backpack 
    for x in range(len(genome)):
        if genome[x] == 1:
            total_weight += ListBoxes[x].get_weight()
            total_importance += ListBoxes[x].get_importance()

    # when total weight is lower than the given limit, the fitness value equals to the total weight
    if total_weight <= 250:
        fitness_value = total_importance
    else : # when total weight is higher, a penalty in the form given below is applied for the fitness value
        fitness_value = total_importance / (total_weight - 250)
    return fitness_value



# picks a pair of individuals from the population
def select_pair(population : List):
    # choices- after population, add [fitness_func(genome) for genome in population] (takes into account-fitness value)
    # return choices(population, k = 2)
    return sample(population, 2) # this method ensures that we don't pair up the same individual



# check if the termination condition is met and if not let the individuals in the generation go through crossover and mutation
def generation_evolution(population, iteration_num):
    
    # check if the termination condition is met
    if solution_reached_check(population, iteration_num):
        fitness_values = [fitness_function(genome) for genome in population]
        maxValue = max(fitness_values)
        indexOfMax = fitness_values.index(maxValue)
        print("Stop generation evolution")
        return population[indexOfMax]

    # pairs up the individuals in the population, and add the pairs to a list
    individual_pairs = []
    for x in (range(len(population)//2)):
        individual_pairs.append(select_pair(population))

    # apply crossover between the individuals in a pair for every single pair
    for x in (range(len(individual_pairs))): 
        individual_pairs[x] = single_crossover(individual_pairs[x][0], individual_pairs[x][1])
        
    # turn the individual pairs list, which is a  list of tuples, to a regular list
    new_generation = list(itertools.chain(*individual_pairs))

    # let mutation occur based on a given probability to every individual in the generation
    new_generation = [mutation(genome, 0.5) for genome in new_generation]

    # apply elitisim by adding the most fit individual in the last generation unchanged to the new generation
    new_generation.append(elitism(population))

    return new_generation # return the new generation

# returns the most fit individual  
def elitism(population):
    fitness_values = [fitness_function(genome) for genome in population]
    maxValue = max(fitness_values)
    indexOfMax = fitness_values.index(maxValue)
    return population[indexOfMax]


# evaluate the current population to check if the termination condition is met 
def solution_reached_check(population, iteration_num):
    if len(population) == 1 or iteration_num > 30: # terminaties the evolution if the number of individual is
        return True                                 # reduced to 1 or the number of previous evolutions reaches 50
        


# halve the generation by 2 and take the half with individuals that have higher fitness values
def generation_cut(population):

    # record the fitness value of each individual in a list
    fitness_values = [fitness_function(genome) for genome in population]

    sorted_population : List

    # zip the population list and fitness values in a list of tuples
    sorted_population = list(zip(population, fitness_values))

    # sort the population in the order of increasing fitness values (lambda expression, sorts the tuple based on the second item of the tuples in the list)
    sorted_population.sort(key = lambda sorted_population: sorted_population[1], reverse = True)

    # take the first half of the generation which have individuals with higher fitness values
    culled_generation = []
    for x in (range(len(sorted_population)//2)):
        sorted_individual = sorted_population[x]
        culled_generation.append(sorted_individual[0])

    #print(culled_generation)
    return culled_generation


# -------------------------------------------------- Operations on a  Generation -------------------------------------------------- #


def run_evolution(num_individuals):    
    number_of_individuals = num_individuals
    
    generation = generate_population(number_of_individuals, 12)

    print("Evolution Number: 0")
    print("Information on the First Generation")
    for x in range(len(generation)):
        print(x+1,". individual's,  Genome:", generation[x]," Fitness Value: " , fitness_function(generation[x]))   
    print("---")

    evolution_num = 0
    while(len(generation) > 1 and evolution_num <= 30):     
        evolution_num += 1  # evolution number is incremented

        generation = generation_evolution(generation, evolution_num) # crossover, and mutation takes place on the current generation

        print("Evolution Number: ", evolution_num)
        print("Information on the Current Generation After Evolution!")
        for x in range(len(generation)):
            print(x+1,". individual's,  Genome:", generation[x]," Fitness Value: " , fitness_function(generation[x]))  
        print("---")


        generation = generation_cut(generation) # generation is culled by 50%

        print("Information on the Current Generation After Culling!")
        for x in range(len(generation)):
            print(x+1,". individual's,  Genome:", generation[x]," Fitness Value: " , fitness_function(generation[x]))  
        print("---")

    return generation  
        

# -------------------------------------------------- Main -------------------------------------------------- #

# run the evolution function and then print the results on the terminal
num_individuals = int(input("Enter a number between 50 - 500 for the number of individuals in the population:") + '\n')
# Note that: As the number of individuals in initial population increase, the genetic algorithm 
# produces a better combination of items in the backpack with higher fitness value. My genetic algorithm
# converges around 200 indivuals and therefore inputting 200 individuals is recommended!
mostFitIndividual = run_evolution(num_individuals)

print("The genome of the most fit individual: ", mostFitIndividual)    # display the genome/chromosome of the most fit combination of items in the backpack

print("The fitness value of the most fit individual: ", fitness_function(mostFitIndividual[0]))     # display the fitness value of the most fit combination of items in the backpack


total_weight = 0                                # calculate the total weight of the most
for x in range(len(mostFitIndividual[0])):      # fit combination of items in the backpack
        if mostFitIndividual[0][x] == 1:
            total_weight += ListBoxes[x].get_weight()

print("The total weight of the most fit combination of item put in the backpack: ", total_weight)     # display the weight of the most fit combination of items in the backpack

















# -------------------------------------------------- TESTING -------------------------------------------------- #





# ---------------------- GENERATION EVOLUTION ---------------------- #


# print("-----------------------------")

# first_generation = generate_population(3, 12)
# print(*first_generation, sep="\n")


# print("-----------------------------")

# individual_pairs = []
# for x in (range(len(first_generation)//2)):
#     individual_pairs.append(select_pair(first_generation))

# print(individual_pairs)


# print("-----------------------------")

# for x in (range(len(individual_pairs))): 
#     individual_pairs[x] = single_crossover(individual_pairs[x][0], individual_pairs[x][1])
        
# print(individual_pairs)


# print("-----------------------------")

# new_generation = list(itertools.chain(*individual_pairs))

# print(new_generation)


# print("-----------------------------")

# new_generation = [mutation(genome, 0.5) for genome in new_generation]

# print(new_generation)


# print("-----------------------------")




# ---------------------- CULLING TEST ---------------------- #



# first_generation = generate_population(5, 12)
# print(*first_generation, sep="\n")

# print("-----------------------------")

# fitness_values = [fitness_function(genome) for genome in first_generation]
# print(*fitness_values, sep="\n")

# print("-----------------------------")

# sorted_population = list(zip(first_generation, fitness_values))
# sorted_population.sort(key = lambda sorted_population: sorted_population[1], reverse = True)

# print(sorted_population)

# new_generation = []
# for x in (range(len(sorted_population)//2)):
#     sorted_individual = sorted_population[x]
#     new_generation.append(sorted_individual[0])
# print(new_generation)


# fitness_values = [fitness_function(genome) for genome in new_generation]
# print(fitness_values)





