"""Simple travelling salesman problem between cities."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp



def create_data_model():
    """Stores the data for the problem."""
    data = {}

    data['distance_matrix'] = [
        [0,	20,	25,	33,	33,	43,	56,	64,	62,	71,	79,	87,	95,	102,	93,	101,	117],	
        [20,0,	19,	35,	43,	51,	66,	73,	68,	79,	86,	94,	101,	108,	98,	102,	118],	
        [25,	19,0,	17,	28,	34,	50,	56,	51,	62,	69,	76,	83,	90,	80,	83,	99],	
        [33,	35,	17,0,	16,	19,	35,	40,	35,	46,	53,	60,	67,	74,	64,	69,	85],	
        [33,	43,	28,	16,0,	10,	24,	31,	29,	38,	46,	54,	62,	70,	61,	70,	85],	
        [43,	51,	34,	19,	10,0,	16,	22,	19,	29,	37,	44,	52,	60,	51,	60,	75],	
        [56,	66,	50,	35,	24,	16,0,	8,	12,	16,	24,	32,	40,	48,	41,	54,	69],	
        [64,	73,	56,	40,	31,	22,	8,0,	8,	8,	16,	24,	32,	40,	33,	47,	61],	
        [62,	68,	51,	35,	29,	19,	12,	8,0,	12,	18,	26,	33,	41,	32,	44,	59],	
        [71,	79,	62,	46,	38,	29,	16,	8,	12,0,	8,	16,	24,	32,	26,	40,	54],	
        [79,	86,	69,	53,	46,	37,	24,	16,	18,	8,0,	8,	16,	24,	18,	34,	47],	
        [87,	94,	76,	60,	54,	44,	32,	24,	26,	16,	8,0,	8,	16,	12,	29,	40],	
        [95,	101,	83,	67,	62,	52,	40,	32,	33,	24,	16,	8,0,	8,	8,	26,	34],	
        [102,	108,	90,	74,	70,	60,	48,	40,	41,	32,	24,	16,	8,0,	12,	24,	29],	
        [93,	98,	80,	64,	61,	51,	41,	33,	32,	26,	18,	12,	8,	12,0,	18,	29],	
        [101,	102,	83,	69,	70,	60,	54,	47,	44,	40,	34,	29,	26,	24,	18,0,	16],	
        [117,	118,	99,	85,	85,	75,	69,	61,	59,	54,	47,	40,	34,	29,	29,	16,0],	
    ]  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

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
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()