import csv, numpy as np
from math import sqrt, ceil
import sys, os

def calc_dist(a, b):
    return sqrt((a['x'] - b['x'])**2 + (a['y'] - b['y'])**2)

infinity = 99999

file_name = 'position/galaxy_pos.csv'

with open(file_name, 'r', encoding='utf-16') as csv_file:

    reader = list(csv.DictReader(csv_file))

    galaxy = [{'x': float(row['x']), 'y': float(row['y'])} for row in reader]
    
    txt_name = file_name.split('.')[0]
    txt_file = open(f'{txt_name}.txt', 'w')

    matrix = np.zeros(shape=(len(galaxy), len(galaxy)))

    for i in range(len(galaxy)):
        matrix[i, i] = infinity
        for j in range(i + 1, len(galaxy)):
            dist = ceil(calc_dist(galaxy[i], galaxy[j]))
            matrix[i, j] = dist
            matrix[j, i] = dist
    
    for i in range(len(galaxy)):
        for j in range(len(galaxy)):
            txt_file.write(f'{int(matrix[i, j])} ')
        txt_file.write(f'\n')

    txt_file.close()
    

