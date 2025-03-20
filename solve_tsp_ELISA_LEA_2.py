# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import cities as ct # Import the cities module
import random 

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm 

        Args:
            chromosome (list[]): a list representing the individual's chromosome
            fitness (float): the individual's fitness (the higher, the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.7):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=200):
        """ Initialize the population with pop_size random Individuals """

        for i in range (pop_size):
            chromosome = ct.default_road(city_dict) # Generate a random guess
            random.shuffle(chromosome) # Generate a random chromosome
            fitness = -ct.road_length(city_dict,chromosome) # Rate the generated chromosome, fitness is now the length of the road
            new_individual = Individual(chromosome, fitness) # Create a new Individual
            self._population.append(new_individual) # Add the new Individual to the population

    def evolve_for_one_generation(self):
        
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """
        population_size = len(self._population)  
        self._population.sort(reverse=True,key= lambda ind: ind.fitness)  # sort the population by descending fitness
        selection_size = int(len(self._population) * self._selection_rate)  
        self._population = self._population[:selection_size]  

        possible_cities = ct.default_road(city_dict)  # Liste complète des villes


        #CROSSOVER PHASE
        for _ in range(population_size - selection_size): # Reproduction (crossover without repetition)
            parent_a, parent_b = random.sample(range(selection_size), 2)  

            chromosome1 = self._population[parent_a].chromosome
            chromosome2 = self._population[parent_b].chromosome

            crossover_point = len(chromosome1) // 2  
            new_chrom = chromosome1[:crossover_point]  

            #iterate through each city in chromosome2  
            for city in chromosome2:
                if city not in new_chrom:     # If the city is not already in new_chrom, add it  
                    new_chrom.append(city)


            # Check if cities are missing and add them at the end
            missing_cities = set(possible_cities) - set(new_chrom)
            new_chrom.extend(missing_cities) #add the missing cites at the end of new chrom
           
            #MUTATION PHASE 
            position1, position2 = random.sample(range(len(new_chrom)), 2) #Generate two random numbers that correspond to two random positions
            new_chrom[position1], new_chrom[position2] = new_chrom[position2], new_chrom[position1]  #swap their values = MUTATION of the chromosome
            new_individual = Individual(new_chrom, -ct.road_length(city_dict, new_chrom)) #create a new individual from the mutated chromosome added to the list of population
            self._population.append(new_individual)

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass 

    def get_best_individual(self):
        """ Return the best Individual of the population """
        self._population.sort(reverse=True)
        return self._population[0]

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        while max_nb_of_generations > 0:
            self.evolve_for_one_generation() #increment the evolution of one generation
            max_nb_of_generations -= 1 #decreament the number of generations remaining
            if threshold_fitness != None: # check if the threshold has been defined before the comparision
                if self.get_best_individual().fitness >= threshold_fitness: # check if the best individual get to the required threshold
                    break#stop the function because we get the final result



city_dict = ct.load_cities("cities.txt")

solver = GASolver() 
solver.reset_population() 
solver.evolve_until()
best = solver.get_best_individual()
print(ct.road_length(city_dict,best.chromosome))
ct.draw_cities(city_dict, best.chromosome)
