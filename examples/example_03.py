from __future__ import print_function
from ortools.linear_solver import pywraplp



def LinearProgrammingExample():
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Create the two variables and let them take on any non-negative value.
    x = solver.NumVar(0, solver.infinity(), 'x')
    y = solver.NumVar(0, solver.infinity(), 'y')

    # Constraint 0: 3x + y >= 6
    constraint0 = solver.Constraint(6, solver.infinity())
    constraint0.SetCoefficient(x, 3)
    constraint0.SetCoefficient(y, 1)

    # Constraint 1: -2x + 3y <= 7
    constraint0 = solver.Constraint(-solver.infinity(), 7)
    constraint0.SetCoefficient(x, -2)
    constraint0.SetCoefficient(y, +3)

    # Constraint 2: x + 3y <= 19
    constraint0 = solver.Constraint(-solver.infinity(), 19)
    constraint0.SetCoefficient(x, 1)
    constraint0.SetCoefficient(y, 3)

    # Constraint 3: 4x - y <= 24
    constraint0 = solver.Constraint(-solver.infinity(), 24)
    constraint0.SetCoefficient(x, 4)
    constraint0.SetCoefficient(y, -1)

    # Constraint 4: 4x - 3y <= 20
    constraint0 = solver.Constraint(-solver.infinity(), 20)
    constraint0.SetCoefficient(x, 4)
    constraint0.SetCoefficient(y, -3)

    # Objective function: 3x + 7y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 7)
    # objective.SetMaximization()
    objective.SetMinimization()

    # Solve the system.
    solver.Solve()
    opt_solution = 3 * x.solution_value() + 7 * y.solution_value()
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    # The value of each variable in the solution.
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    # The objective value of the solution.
    print('Optimal objective value =', opt_solution)


LinearProgrammingExample()