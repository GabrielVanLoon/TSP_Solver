from __future__ import print_function
from ortools.linear_solver import pywraplp
from .classic_solver import ClassicSolver
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Sub-tour elimination(DFJ)
class LazyCuttingPlane(ClassicSolver):
    def __init__(self, distance_matrix, initial_solution=None, timeout=None, verbose=False, name_instance=None):
        super().__init__(distance_matrix, initial_solution, timeout, verbose)
        self.name_instance = name_instance

    def init_constraints(self):
        super().init_constraints()
        # For all sub-sets() less than the number of cities
        for i in range(2, 3):
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
            self.solver.Add(self.solver.Sum(acc) <= length_cycle-1).set_is_lazy(True)
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
            self.solver.Add(self.solver.Sum(acumulator) <= len(acumulator)-1)
            return True
        return False

    # Inicialize variables using Hint
    def set_new_hint(self):
        print("------------set-hint-----------------")
        print(self.final_path)
        if self.initial_solution is not None:
            self.vet_vars = []
            self.vet_init = []
            for i in range(self.n_nodes):
                for j in range(self.n_nodes):
                    self.vet_vars.append(self.x[i,j])
                    self.vet_init.append(self.final_path[i][j])

        # Inicialize variables using Hint
        self.solver.SetHint(self.vet_vars, self.vet_init)

    def print_solution(self):
        [print(u) for u in self.final_path]
        G = nx.DiGraph()
        G.add_edges_from(self.final_path)
        pos = nx.spring_layout(G)
        nx.draw(G, cmap = plt.get_cmap('jet'))
        plt.show()

    def has_time(self):
        """Procure pelas linhas e adicione ao tempo total"""

        total_time = 0.0
        # Open the file in read only mode
        with open((self.name_instance), 'r') as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if "Solving Time" in line:
                    num = float(line.split(" : ")[1])
                    # If yes, then add the line number & line as a tuple in the list

                    if num == 0.0:
                        num += 0.01

                    total_time += num
        # Return list of tuples containing line numbers and lines where string is found
        print(total_time)
        return (total_time < 60 * self.timeout)

    def solve(self):
        if self.solver is None:
            return
        
        # Execute the model and save the results
        self.status = self.solver.Solve()
        self.objective_value =  self.solver.Objective().Value()
        i = 0
        while(i < 100 and self.has_time()):
            # print('The problem does not have an optimal solution in cycle: %d' %(i))
            if(self.block_subpath() is True):
                self.status = self.solver.Solve()
                self.objective_value = self.solver.Objective().Value()
            else:
              break
            i += 1 
            print("Cicle: ", i)
        self.resolve_final_path()
        print("Route: ", self.final_path)

# Execute to test the MTZSolver
if __name__ == '__main__':
    test_data =    [[-1, 1, 5, 17, 1],
                    [1, -1, 7, 5, 9],
                    [5, 7, -1, 3, 8],
                    [17, 5, 3, -1, 2],
                    [1, 9, 8, 2, -1]]
    
    my_solver = LazyCuttingPlane(test_data)
    my_solver.solve()

    [print(u) for u in my_solver.final_path]
    G = nx.DiGraph()
    G.add_edges_from(my_solver.final_path)
    pos = nx.spring_layout(G)
    nx.draw(G, cmap = plt.get_cmap('jet'))
    plt.show()