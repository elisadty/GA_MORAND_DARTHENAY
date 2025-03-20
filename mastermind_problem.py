# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem, Individual
import mastermind as mm
import random 

class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""
    
    def __lt__(self, match =list):
        """Implementation of the less_than comparator operator"""
        self.match = match

    def generate_secrete_code(self, choice, _colors, size): # generate the code for the secret solution 
        secret = [choice(_colors) for _ in range(size)]
        for i in range(self.match.size):
            return random.randint(0, 9)

    def fitness(self, individual: Individual):
        return self.match.evaluate(individual.chromosome)
    
    def crossover(self, parent1: Individual, parent2: Individual):
        crossover_point = random.randint(1, len(parent1.chromosome) - 1)
        return Individual(parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:])

    def mutation(self, individual: Individual):
        for i in range (len(self._population)):
            if random.random() < self._mutation_rate: # Check if the random number generated is below the mutation rate
                chromosome = self._population[i].chromosome #recuperation of chromosome that is at index i in population
                mutated_gene = random.randrange(0, len(chromosome)) # Generate a random gene that would be mutated
                chromosome[mutated_gene] = mm.generate_random_guess() # Mutated
                self._population[i].chromosome = chromosome # Update the chromosome
                self._population[i].fitness = mm.rate_guess(chromosome)

if __name__ == '__main__':

    from ga_solver import GASolver

    match = mm.MastermindMatch(secret_size=6)
    problem = MastermindProblem(match)
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_until()

    print(
        f"Best guess {mm.decode_guess(solver.getBestDNA())} {solver.get_best_individual()}")
    print(
        f"Problem solved? {match.is_correct(solver.get_best_individual().chromosome)}")
