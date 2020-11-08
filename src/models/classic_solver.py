from __future__ import print_function
from ortools.linear_solver import pywraplp

class ClassicSolver:
    def __init__(self, distance_matrix):
        # Variables
        self.distance = distance_matrix
        self.n_nodes = len(distance_matrix)
        self.x = {}
        # Objective Function
        self.function_goal = []
        # Solver Object
        self.solver = None
        self.status = None
        self.objective_value = None
        self.final_path = None

        # Execute initializations
        self.init_solver()
        self.init_variables()
        self.init_constraints()
        self.init_goal()

    def init_solver(self):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')


    def init_variables(self):
        if self.solver is None:
            return
        
        # Inicializate boolean variable x[i, j]
        for position_from in range(self.n_nodes):
            for position_to in range(self.n_nodes):
                if position_from != position_to:
                    self.x[position_from, position_to] = self.solver.IntVar(0, 1, '')
                else:
                    self.x[position_from, position_to] = self.solver.IntVar(0, 0, '')

    def init_constraints(self):
        if self.solver is None:
            return

        # Add consrains that all cities must have an arest leaving
        for i in range(self.n_nodes):
            self.solver.Add(self.solver.Sum( self.x[i, j] for j in range(self.n_nodes) )-self.x[i, i] == 1)

        # Add consrains that all cities must have an arest arriving
        for j in range(self.n_nodes):
            self.solver.Add(self.solver.Sum(self.x[i, j] for i in range(self.n_nodes))-self.x[i, i] == 1)
    
    def init_goal(self):
        if self.solver is None:
            return
    
        # Goal function: Minimize the cicle distance
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                if i != j:
                    self.function_goal.append(self.distance[i][j] * self.x[i, j])

        self.solver.Minimize(self.solver.Sum(self.function_goal))

    def solve(self):
        if self.solver is None:
            return

        # Execute the model and save the results
        self.status = self.solver.Solve()
        self.objective_value =  self.solver.Objective().Value()

    def resolve_final_path(self):
        if self.solver is None:
            return

        # Reset final_path from previous executions
        self.final_path = []

        # Scan all x[i,j] looking where the path is true
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                if i != j and self.x[i,j].solution_value():
                    self.final_path.append([i,j])
        
# Execute to test the ClassicSolver
if __name__ == '__main__':
    test_data =    [[-1, 1, 5, 17, 1],
                    [1, -1, 7, 5, 9],
                    [5, 7, -1, 3, 8],
                    [17, 5, 3, -1, 2],
                    [1, 9, 8, 2, -1]]
    
    my_solver = ClassicSolver(test_data)
    my_solver.solve()
    
    if  my_solver.status == pywraplp.Solver.OPTIMAL:
        my_solver.resolve_final_path()

        print('Found Solution')
        print('Objective value:', my_solver.objective_value)
        print('Variables: ', my_solver.final_path)
    else:
        print('The problem does not have an optimal solution.')