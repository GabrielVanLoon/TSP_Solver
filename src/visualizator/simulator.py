#!/usr/bin/env python3
import sys, os
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import numpy as np

from src.parser.coord_to_matrix import make_matrix_dist

trackingPath = 'data/tracking/'

# Options map
solver_translator = {'': None, 'NN (Nearest Neighbor)': 'nn', 'Christofides': None}

class Simulator:
    """
        distance_matrix : (nxn) represent the actual graph
        iterations      : (dict) solutions changging though iteration 
    """
    def __init__(self, series_pick = '', initial_node = 0, initial_solution = [], solver = ''):
        self.series_pick = series_pick          # the series choosen by user
        self.distance_matrix = None             # the nodes and edges
        self.nx_graph = None
        self.iterations = {}                    # id, solution, objective_value, time_elapsed

        # Initial wConfigurations
        self.initial_node = initial_node

        # Animations
        self.iteration = 0

        # Class of the solver
        self.solver = solver_translator[solver]

        print("Simulator Parameters uptadeted.")


    def load_nx_graph(self):
        self.nx_graph = nx.complete_graph(100)


    def solving(self):
        '''
            Call the solver for the series

            This function should be called when series or solver changes
        '''
        print("Solving...")
        self.load_nx_graph()

        # Validation
        if self.series_pick == '':
            return [False, 'Selecione um caso teste.']
        
        if self.solver == None:  
            return [False, 'Selecione um algoritmo.']

        # Execution
        if self.solver == "nn":
            os.system("./main.py visualization -i {0} -s {1}".format(self.series_pick, self.solver))
            self.iterations = self.read_tracking(trackingPath + self.series_pick + '_' + self.solver + '.txt')

        return [True, '']


    def render_instance(self, iteration):
        """
            Render a networkx graph in screen
        """
        print(iteration)
        print("Changed")

        # Translate to pyvis network
        h, w = 500, 750
        nt = Network(f'{h}px', f'{w}px',
                    font_color='white')
        nt.from_nx(self.nx_graph)
        nt.toggle_physics(False)
        path = f'network.html'
        nt.save_graph(path)

        HtmlFile = open(path, 'r')  # , encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height=h * 1.1, width=w * 1.1)
        print("Changed")


    def fromstring(self, path_string):
        '''
            This function parse the matrix in string to a array matrix in python
        '''
        num_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        arr_list = list(path_string)

        matrix = []
        row = []

        for i in range(0, len(arr_list)):
            try:
                if(len(row) == 2):
                    matrix.append(row)
                    row = []
                if(int(arr_list[i]) in num_set):
                    row.append(int(arr_list[i]))
            except:
                continue

        return matrix


    def read_tracking(self, route_filename):
        '''
        Parametros
        ----------
            my_solver : Class solver
                Instancia com nós, arestas e sequências de soluções para cada iteração.
            coord_filename : str
                Arquivo csv que tem as coordenadas (id, x, y). Estes arquivos com as coordenadas
                estao na pasta '/data/coord'
            route_filename : str
                Arquivo csv que sera criado para armazenar as rotas
        '''

        iterations = dict()
        # open and read file
        try:
            file = open(route_filename)
            iterations = file.readlines()
            file.close()
        except:
            print("The input file does not exist.")
            return 0
            
        # For each iteration
        for it, iteration in enumerate(iterations):
            
            # Read the haeder
            if it == 0:
                continue
            
            id_iteration, path_string, time_elapsed = iteration.split('-')

            iterations[int(id_iteration)] = { 'path': self.fromstring(path_string), 'time_elapsed': time_elapsed }
        return iterations


