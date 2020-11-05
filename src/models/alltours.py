"""
    Generate all tours and pick the one with least cost
    O(n!)
"""
import sys, os
import itertools
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import helper

NUM_CITIES = 0

def tour_length(tour, dist):
    """
        Sum of a distance of tour
    """
    sum_tour = 0

    for i in range(0, len(tour)):
        sum_tour = sum_tour + dist[tour[i]][tour[i-1]]
    return sum_tour

def shortest_tour(tours, dist):
    """
        Take least sum of the tours : sum(tours)
    """
    length_tours = []
    for i in np.arange(len(tours)):
        length_tours.append(tour_length(tours[i], dist)) 
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

def tsp_alltours(num_cities, dist):
    """
        Return shortest cicle such that all cities are visited.
    """
    return shortest_tour(alltours(num_cities), dist)

def main():
    dist = helper.load_data()
    NUM_CITIES = len(dist)

    print(tsp_alltours(NUM_CITIES, dist))

if __name__ == '__main__':
    main()