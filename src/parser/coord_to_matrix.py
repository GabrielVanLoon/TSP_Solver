import csv
import numpy as np
from   math  import sqrt, ceil

def calc_dist(a, b):
    return int(sqrt((a['x'] - b['x'])**2 + (a['y'] - b['y'])**2))


def read_csv_coord(csv_filename, encoder = 'utf-8'):
    with open(csv_filename, 'r', encoding=encoder) as csv_file:

        reader = list(csv.DictReader(csv_file))

        coord = [{'x': float(row['x']), 'y': float(row['y'])} for row in reader]
        return coord


def make_matrix_dist(csv_filename, txt_filename, num_diag = 0.0, encoder = 'utf-8'):

    '''
    Cria um arquivo txt com a matriz de distancias entre as coordenadas
    a partir de um arquivo csv com coordenadas (/data/coord/coord.csv)

    Parametros
    ----------
        csv_filename : str
            Nome do arquivo csv onde estao as coordenadas das localizacoes
        txt_filename : str
            Nome do arquivo txt que sera criado para armazenar a matriz de 
            distancias entre as coordenadas 
        num_diag : int
            Valor da diagonal na matriz de distancias entre as coordenadas
    '''

    with open(csv_filename, 'r', encoding=encoder) as csv_file:

        reader = list(csv.DictReader(csv_file))

        coord = [{'x': float(row['x']), 'y': float(row['y'])} for row in reader]
        n_coord = len(coord)

        with open(txt_filename, mode='w') as txt_file:

            matrix = np.zeros(shape=(n_coord, n_coord))

            for i in range(n_coord):
                matrix[i, i] = num_diag
                for j in range(i + 1, n_coord):
                    dist = calc_dist(coord[i], coord[j])
                    matrix[i, j] = dist
                    matrix[j, i] = dist
            
            for i in range(n_coord):
                for j in range(n_coord):    
                    txt_file.write(f'{matrix[i, j]}\t')
                txt_file.write(f'\n')