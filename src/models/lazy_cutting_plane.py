from __future__ import print_function
from ortools.linear_solver import pywraplp
from .classic_solver import ClassicSolver
import numpy as np

# Sub-tour elimination(DFJ)
class LazyCuttingPlane(ClassicSolver):
    def __init__(self, distance_matrix):
        super().__init__(distance_matrix)

    def init_constraints(self):
        super().init_constraints()

        if(self.n_nodes > 3):
            self.add_res(2);
            self.add_res(3);
   
    def add_res(self, n):
        # Auxiliary array of cities [0, ..., n]
        next_node = list(range(0, self.n_nodes))
        
        # For all paths, check sub-cicle of length i
        for j in range(0, self.n_nodes):
            initial = next_node.pop(0)
            self.all_sub_cycles([], initial, initial, 1, n, next_node)

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
            self.all_sub_cycles(acc, initial, next, nivel + 1, length_cycle, next_node)
            next_node.append(next)
            acc.pop(-1)
        return 

    # def all_sub_cycles(self, acc, initial, actual, nivel, length_cycle, next_node):
        # '''
        #     Add restriction to cycles of length lenght_cycle
        #     __________________________
        #     Example length_cycle = 2
        #     x[ij] + x[ji] <= 2
        #     __________________________
        #     Example length_cycle = 3
        #     x[ij] + x[jk] + x[ki] <= 3
        # '''

        # if(nivel == length_cycle):
        #     acc.append(self.x[actual, initial])
        #     self.solver.Add(self.solver.Sum(acc) <= length_cycle-1)
        #     acc.pop(-1)
        #     return 
        
        # # TODO: check if conection from actual to j next

        # # for all remaning nodes, add restriction
        # for j in range(len(next_node)):
        #     next = next_node.pop(0)
        #     acc.append(self.x[actual, next])
        #     self.all_sub_cycles(acc, initial, next, nivel + 1, length_cycle, next_node)
        #     next_node.append(next)
        #     acc.pop(-1)
        # return 


    def has_sub_cycle(self, acumulator, path):

        # Inicialization of variables
        queue = [0]
        vis = np.zeros([self.n_nodes])
        is_sub_path = False
        while(is_sub_path is not True and len(queue) > 0):
            front = queue.pop()
            for i in range(self.n_nodes):
                if(self.x[front, i].solution_value() == 1):
                    if(vis[i] == 0):
                        vis[i] = 1
                        queue.append(i)
                        acumulator.append(self.x[front, i])
                        path.append([front, i])
                    else:
                        if(len(acumulator) < self.n_nodes):
                            is_sub_path = True
                    break   
        
        return is_sub_path

    # If find a sub cylces, add a constrain to this sub-cycle
    def block_subpath(self):
        self.resolve_final_path()
        acumulator = []
        path = []
        if(self.has_sub_cycle(acumulator, path) is True):
            # print(path)
            self.solver.Add(self.solver.Sum(acumulator) <= len(acumulator)-1)
            # self.add_res(len(acumulator))
            return True
        return False

    def solve(self):
        if self.solver is None:
            return
        
        # Execute the model and save the results
        self.status = self.solver.Solve()
        self.objective_value =  self.solver.Objective().Value()
        
        max_cycles = 100
        i = 0
        while(i < max_cycles):
            # print('The problem does not have an optimal solution in cycle: %d' %(i))
            print("The upper bound solution is %d " % (self.objective_value))
            if(self.block_subpath() is True):
                self.status = self.solver.Solve()
                self.objective_value =  self.solver.Objective().Value()
            else:
                break
            i += 1 

# Execute to test the MTZSolver
if __name__ == '__main__':
    test_data =    [[-1, 1, 5, 17, 1],
                    [1, -1, 7, 5, 9],
                    [5, 7, -1, 3, 8],
                    [17, 5, 3, -1, 2],
                    [1, 9, 8, 2, -1]]
    
    my_solver = LazyCuttingPlane(test_data)
    if(self.n_nodes > 3):
        my_solver.add_res(2);
        my_solver.add_res(3);

    max_cycles = 4
    i = 0
    while(i < max_cycles):
        my_solver.solve()
        if  my_solver.status == pywraplp.Solver.OPTIMAL:
            my_solver.resolve_final_path()

            print('Found Solution in iteration %d' %(i))
            print('Objective value:', my_solver.objective_value)
            print('Variables: ', my_solver.final_path)
            break
        else:
            print('The problem does not have an optimal solution in cycle: %d .' %(i))
            my_solver.block_subpath();
            break
        print("The upper bound solution is " + my_solver.objective_value)
        i += 1
    