from __future__ import print_function
from ortools.linear_solver import pywraplp
import itertools
import numpy as np

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import helper


class BruteForcer:
    def __init__(self, distance_matrix):
        # Variables
        self.distance = distance_matrix
        self.n_nodes = len(distance_matrix)
        self.permutations = None
        
        # Solver Objects
        self.status = None
        self.objective_value = None
        self.best_path_index = 0
        self.final_path = None

    def solve(self):
        # First generate permutations of tours O(n!)
        self.generate_all_tours()

        # for each tour get the distance and save the best        
        best_distance = -1
        best_index    = 0

        for i in np.arange(len(self.permutations)):
            i_distance = self.calc_tour_distance(i)
            if best_distance == -1 or i_distance < best_distance:
                best_distance = i_distance
                best_index = i
                
        self.objective_value = best_distance
        self.best_path_index = best_index
        self.status = pywraplp.Solver.OPTIMAL
        
    def resolve_final_path(self):
        # Do nothing, keep to maintain the sabe interface
        return
    
    def generate_all_tours(self):
        if self.permutations is not None:
            return
        
        # Generate all indexes [1,2,3, ... , n]
        cities = np.arange(self.n_nodes)

        # Generate all permutations
        tours = []
        for tour in itertools.permutations(cities): 
            tours.append(np.array(tour))

        self.permutations = np.array(tours)#.copy()

    def calc_tour_distance(self, p):
        # Get the sum of the full path
        sum_tour = 0
        for i in range(0, len(self.permutations[p])-1):
            sum_tour += self.distance[self.permutations[p][i]][self.permutations[p][i+1]]

        # Get the distance of the last element with the first (close the cicle)
        sum_tour += self.distance[self.permutations[p][-1]][self.permutations[p][0]]

        return sum_tour


# Execute to test the MTZSolver
if __name__ == '__main__':
    # test_data =    [[-1, 1, 5, 17, 1],
    #                 [1, -1, 7, 5, 9],
    #                 [5, 7, -1, 3, 8],
    #                 [17, 5, 3, -1, 2],
    #                 [1, 9, 8, 2, -1]]
    
    test_data = helper.load_data("7.txt")
    my_solver = BruteForcer(test_data)
    my_solver.solve()
    
    if  my_solver.status == pywraplp.Solver.OPTIMAL:
        my_solver.resolve_final_path()

        print('Found Solution')
        print('Objective value:', my_solver.objective_value)
        print('Variables: ', my_solver.final_path)
    else:
        print('The problem does not have an optimal solution.')