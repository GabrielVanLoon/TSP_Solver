from __future__ import print_function
from ortools.linear_solver import pywraplp
from .classic_solver import ClassicSolver

# Sub-tour elimination(DFJ)
class CuttingPlane(ClassicSolver):
    def __init__(self, distance_matrix):
        super().__init__(distance_matrix)

    def init_constraints(self):
        super().init_constraints()

        # Auxiliary array of cities [0, ..., n]

        # For all sub-sets() less than the number of cities
        for i in range(2, int(self.n_nodes/2)+1):
            next_node = list(range(0, self.n_nodes))
            # For all paths, check sub-cicle of length i
            for j in range(0, self.n_nodes):
                initial = next_node.pop(0)
                self.all_sub_cycles([], initial, initial, 1, i, next_node)

    def all_sub_cycles(self, acc, initial, actual, nivel, length_cycle, next_node):
        '''
            Add restriction to cycles of length lenght_cycle
            __________________________
            Example length_cycle = 2
            x[ij] + x[ji] <= 2
            __________________________
            Example length_cycle = 3
            x[ij] + x[jk] + x[ki] <= 3
        '''

        if(nivel == length_cycle):
            acc.append(self.x[actual, initial])
            self.solver.Add(self.solver.Sum(acc) <= length_cycle-1)
            acc.pop(-1)
            return 
        
        # TODO: check if conection from actual to j next

        # for all remaning nodes, add restriction
        for j in range(len(next_node)):
            next = next_node.pop(0)
            acc.append(self.x[actual, next])
            print(actual, end=' ')
            self.all_sub_cycles(acc, initial, next, nivel + 1, length_cycle, next_node)
            next_node.append(next)
            acc.pop(-1)
        return 

# Execusute to test the MTZSolver
if __name__ == '__main__':
    test_data =    [[-1, 1, 5, 17, 1],
                    [1, -1, 7, 5, 9],
                    [5, 7, -1, 3, 8],
                    [17, 5, 3, -1, 2],
                    [1, 9, 8, 2, -1]]
    
    my_solver = CuttingPlane(test_data)
    my_solver.solve()
    
    if  my_solver.status == pywraplp.Solver.OPTIMAL:
        my_solver.resolve_final_path()

        print('Found Solution')
        print('Objective value:', my_solver.objective_value)
        print('Variables: ', my_solver.final_path)
    else:
        print('The problem does not have an optimal solution.')