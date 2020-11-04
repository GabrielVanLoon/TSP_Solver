"""
    Generate all tours and pick the one with least cost
"""
import itertools
import numpy as np

INF = np.Inf

dist = [
    [0, 1, 2],
    [1, 0, 3],
    [2, 3, 0]
]

NUM_CITIES = 3

def tour_length(tour):
    """
        Sum of a distance of tour
    """
    sum_tour = 0
    for i in range(len(tour)):
        sum_tour = sum_tour + dist[tour[i]][tour[i-1]]
    return sum_tour

def shortest_tour(tours):
    """
        Take least sum of the tours : sum(tours)
    """
    length_tours = []
    for i in np.arange(len(tours)):
        length_tours.append(tour_length(tours[i])) 
    return np.min(length_tours)
    
def alltours(num_cities):
    """
        @return all permutations
        Example:
                [[0 1 2]
                [0 2 1]
                [1 0 2]
                [1 2 0]
                [2 0 1]
                [2 1 0]]
    """
    cities = np.arange(num_cities)              # [1, 2, 3, ...]
    
    tours = []
    for tour in itertools.permutations(cities): 
        tours.append(np.array(tour))

    return np.array(tours)

def tsp_alltours(num_cities):
    return shortest_tour(alltours(num_cities))

def main():
    print(tsp_alltours(NUM_CITIES))

