# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import mastermind as mm
import random 
MATCH = mm.MastermindMatch(secret_size=4) # Create a MastermindMatch object

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
    def __init__(self, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """

        for i in range (pop_size):
            chromosome = MATCH.generate_random_guess() # Generate a random guess
            fitness = MATCH.rate_guess(chromosome) # Rate the generated chromosome 
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
        #SELECTION PHASE
        population_size = len(self._population) # Get the population size
        self._population.sort(reverse=True) # Sort the population in descending order
        selection_size = int(len(self._population) * self._selection_rate) # Calculate the selection size
        self._population = self._population[:selection_size] # Remove the less adapted Individuals

        #CROSSOVER PHASE
        for i in range(population_size - selection_size): # Create new Individuals
            parent_a = random.randint(0,selection_size -1) # Generate a list composed of random number
            parent_b = random.randint(0, selection_size - 1)
            
            #If two parents are equal, we generate parent_b again
            while parent_a == parent_b:
                parent_b = random.randint(0, selection_size - 1)

            chromosome1 = self._population[parent_a].chromosome #generate a chomosome based of parent_a
            chromosome2 = self._population[parent_b].chromosome #generate a chomosome based of parent_b
            crossover_point = random.randrange(0, len(chromosome1))  # Generate a random number 
            new_chrom = chromosome1[0:crossover_point] + chromosome2[crossover_point:] # Create a new chromosome: first half of chrom1 and second half of chrom2
            new_individual = Individual(new_chrom, MATCH.rate_guess(new_chrom)) # Create a new Individual
            self._population.append(new_individual) # Add the new Individual to the population

        #MUTATION PHASE
        for i in range (len(self._population)):
            if random.random() < self._mutation_rate: # Check if the random number generated is below the mutation rate
                chromosome = self._population[i].chromosome #recuperation of chromosome that is at index i in population
                mutated_gene = random.randrange(0, len(chromosome)) # Generate a random gene that would be mutated
                chromosome[mutated_gene] = MATCH.generate_random_guess() # Mutated
                self._population[i].chromosome = chromosome # Update the chromosome
                self._population[i].fitness = MATCH.rate_guess(chromosome) # Update the fitness


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
        # 
        while max_nb_of_generations > 0: 
            self.evolve_for_one_generation() #increment the evolution of one generation
            max_nb_of_generations -= 1 #decreament the number of generations remaining
            if self.get_best_individual().fitness >= threshold_fitness: # check if the best individual get to the required threshold
                break #stop the function because we get the final result


#solve the match
solver = GASolver() 
solver.reset_population() 
solver.evolve_until(threshold_fitness=MATCH.max_score()) 
print(solver.get_best_individual())
