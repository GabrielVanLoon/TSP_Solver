"""Simple travelling salesman problem between cities."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import logging
import sys

def create_data_model(dist_matrix):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = dist_matrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data
def total_cost(dist_matrix, route):
    cost = 0.0
    for node in range(0, len(route) - 1):
        cost += dist_matrix[route[node]][route[node + 1]]
    cost += dist_matrix[route[-1]][route[0]]
    return cost


def print_solution(dist_matrix, manager, routing, solution):
    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
    print("Route: ", route)
    print("A Solution was found\nObjective value: ", total_cost(dist_matrix, route))


def Christofides(dist_matrix, timeout=None):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(dist_matrix)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
       
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES)
    search_parameters.solution_limit = 1
    search_parameters.log_search = True

    if timeout is not None:
        search_parameters.time_limit.seconds = 60 * timeout
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    # Print solution on console.
    print("Solver status: ", routing.status())
    if solution:
        print_solution(dist_matrix, manager, routing, solution)
    else:
        print('No solution was found. :(')
