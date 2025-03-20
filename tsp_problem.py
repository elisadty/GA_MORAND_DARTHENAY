# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem
import cities as ct

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    pass # REPLACE WITH YOUR CODE


if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = ct.load_cities("cities.txt")
    problem = TSProblem()
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()
    ct.draw_cities(city_dict, solver.getBestIndiv().chromosome)
