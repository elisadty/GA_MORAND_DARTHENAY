# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""

import cities as ct
import random

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem: #specicif of the problem
    """Defines a Genetic algorithm problem to be solved by ga_solver"""
    
    def generate_secrete_code(self):
        pass

    def fitness(self, individual: Individual):
        pass

    def crossover(self, parent1: Individual, parent2: Individual):
        pass

    def mutation(self, individual: Individual):
        pass
    

class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self):
        """ Initialize the population with pop_size random Individuals """
        self.population = [] 
        for i in range(self.pop_size):
            new_individual = Individual(self.problem.generate_random_solution())
            new_individual.fitness = self.problem.evaluate_fitness(new_individual)  
            self.population.append(new_individual) 

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
        #selection part
        self.population.sort(reverse = True) # sort the population in a decreasing order
        survivor = self.population[:int(len(self.population) * self._selection_rate)] # keep the percentage of the population decided by selection rate
        new_population = survivor[:]
        
        while len(new_population) < self.pop_size:
            #reproduction
            parent1, parent2 = random.sample(survivor, 2)
            new_chromosome = self.problem.crossover(parent1, parent2)

            #mutation
            if random.random() < self.mutation_rate:
                self.problem.mutate(new_chromosome)
            new_chromosome.fitness = self.problem.evaluate_fitness(new_chromosome)
            new_population .append(new_chromosome)
        
        self.population = new_population


    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """

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
            if threshold_fitness != None: #check if the threshold has been defined before the comparision
                if self.get_best_individual().fitness >= threshold_fitness: #check if the best individual get to the required threshold
                    break #stop the function because we get the final result
