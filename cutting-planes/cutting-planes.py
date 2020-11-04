"""
    The TSP solved with Cutting Plane formulation
"""
from __future__ import print_function
from ortools.linear_solver import pywraplp
import numpy as np

def create_data_array(solver):

    # infinity value
    INF = solver.infinity()

    cost = [
        [INF, 5, 3, 17, 1],
        [5, INF, 6, 5, 9],
        [3, 6, INF, 3, 3],
        [17, 5, 3, INF, 2],
        [1, 9, 3, 2, INF]]
    return cost

def create_data_model():
    """
    """

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    cost = create_data_array()
    rows = len(cost)
    cols = len(cost[0])

    # Inicializate boolean variable x[i, j]     
    x = {}
    for position_from in range(rows):
        for position_to in range(cols):
            x[i, j] = solver.IntVar(0, 1, '')

    # Add consrains that all cities must have an arest leaving
    for i in range(n):
        solver.Add(solver.Sum(x[i, j] for j in range(n)) == 1)

    # Add consrains that all cities must have an arest arriving
    for j in range(n):
        solver.Add(solver.Sum(x[i, j] for i in range(n)) == 1)


def main():
    create_data_model()