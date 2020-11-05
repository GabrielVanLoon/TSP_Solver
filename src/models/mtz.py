"""
    TSP solver
    The Miller, Tucker and Zemlin (MTZ) formulation
"""
from __future__ import print_function
from ortools.linear_solver import pywraplp

import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import helper

def create_data_model():

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Cost[i, j] : cost to go from i to j
    costs = helper.load_data()
    n_nodes = len(costs)

    # # Inicializate boolean variable x[i, j]
    # x[i, j] is one if there a segment from i to j     
    x = {}
    for position_from in range(n_nodes):
        for position_to in range(n_nodes):
            x[position_from, position_to] = solver.IntVar(0, 1, '')

    # # Inicializate u real variable from 1, n
    # Sub-tour elimination(MTZ)
    u = {}
    for i in range(n_nodes):
        u[i] = solver.NumVar(0, n_nodes, '')

    # Subject to:

    # # Add consrains that all cities must have an arest leaving
    for i in range(n_nodes):
        solver.Add(solver.Sum(x[i, j] for j in range(n_nodes)) == 1)

    # # Add consrains that all cities must have an arest arriving
    for j in range(n_nodes):
        solver.Add(solver.Sum(x[i, j] for i in range(n_nodes)) == 1)

    # # Add constrains MTZ to sub-tour elimination
    for i in range(1, n_nodes):
        for j in range(1, n_nodes):
            if(i != j):
                solver.Add(u[i] - u[j] + n_nodes*x[i, j] <= n_nodes - 1)

    # # Goal function min
    function_goal = []
    for i in range(n_nodes):
        for j in range(n_nodes):
            function_goal.append(costs[i][j] * x[i, j])

    # Set goal function to minimizate
    solver.Minimize(solver.Sum(function_goal))
    
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
    else:
        print('The problem does not have an optimal solution.')

def main():
    create_data_model()

if __name__ == '__main__':
    main()
