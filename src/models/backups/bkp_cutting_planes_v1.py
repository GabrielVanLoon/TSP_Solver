"""
    TSP Solver
    The Dantzig, Fulkerson and Johnson (DFJ) formulation

    This version apply half of the constrains
"""
from __future__ import print_function
from ortools.linear_solver import pywraplp

import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import helper

x = {}
def all_sub_cycles(acc, initial, actual, nivel, length_cycle, next_node, n_nodes, solver):
    """
        Add restriction to cycles of length lenght_cycle
        __________________________
        Example length_cycle = 2

        x[ij] + x[ji] <= 2
        __________________________
        Example length_cycle = 3

        x[ij] + x[jk] + x[ki] <= 3
    """
    if(nivel == length_cycle):
        acc.append(x[actual, initial])
        solver.Add(solver.Sum(acc) <= length_cycle-1)
        acc.pop(-1)
        return 
    
    # TODO: check if conection from actual to j next
    # for all remaning nodes, add restriction
    for j in range(len(next_node)):
        next = next_node.pop(0)
        acc.append(x[actual, next])
        all_sub_cycles(acc, initial, next, nivel + 1, length_cycle, next_node, n_nodes, solver)
        next_node.append(next)
        acc.pop(-1)
    return 

def generate_constrains( n_nodes, solver):
    """
        This will eliminate all subtours adding the constrains of DFJ
    """

    # Auxiliary array of cities [0, ..., n]
    next_node = list(range(0, n_nodes))
    
    # For all sub-sets() less than the number of cities
    for i in range(2, int(n_nodes/2)+1):

        # For all paths, check sub-cicle of length i
        for j in range(0, n_nodes):
            initial = next_node.pop(0)
            all_sub_cycles([], initial, initial, 1, i, next_node.copy(), n_nodes, solver)
            next_node.append(initial)
            

def create_data_model():
    
    costs = helper.load_data()
    n_nodes = len(costs)

     # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # # Inicializate boolean variable x[i, j]
    # x[i, j] is one if there a segment from i to j     
    for position_from in range(n_nodes):
        for position_to in range(n_nodes):
            x[position_from, position_to] = solver.IntVar(0, 1, '')

    # Subject to:

    # # Add consrains that all cities must have an arest leaving
    for i in range(n_nodes):
        solver.Add(solver.Sum(x[i, j] for j in range(n_nodes)) == 1)

    # # Add consrains that all cities must have an arest arriving
    for j in range(n_nodes):
        solver.Add(solver.Sum(x[i, j] for i in range(n_nodes)) == 1)

    # # Add constrains DFJ to sub-tour elimination
    generate_constrains(n_nodes, solver)
    print('Number of constraints =', solver.NumConstraints())

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
