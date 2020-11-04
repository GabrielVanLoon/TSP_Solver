from __future__ import print_function
from ortools.linear_solver import pywraplp
import numpy as np

n = 4

def create_data_array():
    cost = [
        [90, 80, 75, 70],
        [75, 85, 55, 65],
        [125, 95, 125, 95],
        [45, 110, 95, 115]
    ]
    return cost

cost = create_data_array()

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')

# x[i, j] corresponde aos xij do problema, e sao 0 ou 1
x = {}
for i in range(n):
    for j in range(n):
        x[i, j] = solver.IntVar(0, 1, '')

for i in range(n):
    solver.Add(solver.Sum(x[i, j] for j in range(n)) == 1)

# função objetivo
# print(np.dot((x[0, j] for j in range(n)), cost[0][:]))
function = []
for i in range(n):
    for j in range(n):
        function.append(cost[i][j] * x[i, j])

solver.Minimize(solver.Sum(function))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    for i in range(0, n):
        for j in range(0, n):
            if(x[i, j].solution_value() == 1):
                print('Worker %d assigned to task %d.  Cost = %d' % (i, j, cost[i][j]))
else:
    print('The problem does not have an optimal solution.')
