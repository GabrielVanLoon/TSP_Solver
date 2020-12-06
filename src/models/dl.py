from __future__ import print_function
from ortools.linear_solver import pywraplp
from .classic_solver import ClassicSolver

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import helper

# Sub-tour elimination(MTZ)
class DLSolver(ClassicSolver):
    def __init__(self, distance_matrix, initial_solution=None, timeout=None, verbose=False):
        super().__init__(distance_matrix, initial_solution, timeout, verbose)
        # New Variables
        self.u = {}

    def init_variables(self):
        super().init_variables()

        # Inicializate u real variable from 1, n
        self.u = {}
        for i in range(self.n_nodes):
            self.u[i] = self.solver.NumVar(1, self.n_nodes, '')

    def init_constraints(self):
        super().init_constraints()

        # Add constrains MTZ to sub-tour elimination
        for i in range(1, self.n_nodes):
            for j in range(1, self.n_nodes):
                if i != j:
                    self.solver.Add(self.u[i] - self.u[j] + ((self.n_nodes-1)*self.x[i, j]) + ((self.n_nodes-3)*self.x[j, i]) <= self.n_nodes - 2)
            
            self.solver.Add(1 + ((self.n_nodes-3)*self.x[i, 0]) + self.solver.Sum(self.x[j, i] for j in range(1, self.n_nodes)) 
                            <= self.u[i] <= 
                                (self.n_nodes - 1 - ((self.n_nodes - 3)*self.x[0, i]) - self.solver.Sum(self.x[i, j] for j in range(1, self.n_nodes)))
                            )

# Execute to test the MTZSolver
if __name__ == '__main__':
    # test_data =    [[-1, 1, 5, 17, 1],
    #                 [1, -1, 7, 5, 9],
    #                 [5, 7, -1, 3, 8],
    #                 [17, 5, 3, -1, 2],
    #                 [1, 9, 8, 2, -1]]
    
    test_data = helper.load_data("7.txt")
    my_solver = MTZSolver(test_data)
    my_solver.solve()
    
    if  my_solver.status == pywraplp.Solver.OPTIMAL:
        my_solver.resolve_final_path()

        print('Found Solution')
        print('Objective value:', my_solver.objective_value)
        print('Variables: ', my_solver.final_path)
    else:
        print('The problem does not have an optimal solution.')