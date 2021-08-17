#!/usr/bin/env python3
import sys, os
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import numpy as np

from src.parser.coord_to_matrix import (make_matrix_dist, read_csv_coord)
from src.helper import load_data

trackingPath = 'data/tracking/'
distPath = 'data/distances/'
coordPath = 'data/coord/'

# Options map
solver_translator = {'': None, 'NN (Nearest Neighbor)': 'nn', 'Christofides': None}

class Simulator:
    """
        distance_matrix : (nxn) represent the actual graph
        iterations      : (dict) solutions changging though iteration 
    """
    def __init__(self, series_pick, solver, initial_node = 0, initial_solution = []):
        # Simulation inicial configs
        self.series_pick        = series_pick      # the series choosen by user
        self.nx_graph           = None             # Networkx instance
        self.iterations         = {}               # id, solution, objective_value, time_elapsed
        self.solver = solver_translator[solver]    # Algo of the solver
        
        # Load discente matrix with distace matrix .txt file
        self.distance_matrix = load_data(distPath + self.series_pick + '.txt')  
    
        # Initial wConfigurations
        self.initial_node = initial_node

        # Animations
        self.iteration = 0    

        # Simulator style options
        self.circle_bool        = True
        self.hide_edges_bool    = False
        self.hide_weight        = False

        print("Simulator Parameters uptadeted.")


    def load_nx_graph(self):
        # Load node positions
        coords = read_csv_coord(coordPath + self.series_pick + '.csv')
        
        # Create a graph with the distance matrix
        self.nx_graph = nx.empty_graph(len(coords))  # create initial empty graph

        # Add nodes to networkx
        for idx, coord in enumerate(coords):
            for k, v in {'label': idx,
                 'physics': False,
                 'x': coord['x'] * 2.0,
                 'y': coord['y'] * 2.0,
                 'size': 2,
                 'shape': 'circle' if self.circle_bool else 'dot',
                 'color': 'blue',
                 }.items():

                self.nx_graph.nodes[idx][k] = v

            # Show edges if the checkbox is unckecked
            if self.hide_edges_bool == False:
                for i in range(0, idx-1):
                    label = ''
                    if self.hide_weight == False and self.distance_matrix[i][idx] != 0:
                        label = f'{int(self.distance_matrix[i][idx])}'
                    self.nx_graph.add_edge(i, idx, width=1, color='rgb(100,100,100)', label=label)
        


    def load_solution(self, iteration):
        return


    def calling_solver(self):
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


    def render_instance(self, iteration, circle_bool, hide_edges_bool, hide_weight):
        """
            Render a networkx graph in screen
        """
        print("Changed to: ", iteration)

        # If some propriety change, update value and reload the Networx Graph
        if self.circle_bool != circle_bool or self.hide_edges_bool != hide_edges_bool or self.hide_weight != hide_weight:
            self.circle_bool        = circle_bool
            self.hide_edges_bool    = hide_edges_bool
            self.hide_weight        = hide_weight
            self.load_nx_graph()

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
            
            id_iteration, path_string, time_elapsed, objective_value = iteration.split('-')

            iterations[int(id_iteration)] = { 'path': self.fromstring(path_string), 'time_elapsed': time_elapsed, 'objective_value': objective_value }
        
        return iterations


