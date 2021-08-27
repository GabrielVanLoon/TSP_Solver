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
solver_translator = {'': None, 'Opcional': None, 'NN (Nearest Neighbor)': 'nn', 
                        'Christofides': 'chris', 'Two Opt': '2opt'}

class Solver:
    """
        distance_matrix : (nxn) represent the actual graph
        iterations      : (dict) solutions changging though iteration 
    """
    def __init__(self, series_pick, solver, initial_node = 0, initial_solution = []):
        # Simulation inicial configs
        self.series_pick        = series_pick      # the series choosen by user
        self.nx_graph_default   = None             # Networkx instance
        self.nx_graph           = None             # Networkx instance
        self.iterations         = {}               # id, solution, objective_value, time_elapsed
        self.coords             = {}
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
        self.coords = read_csv_coord(coordPath + self.series_pick + '.csv')
        
        # Create a graph with the distance matrix
        self.nx_graph = nx.empty_graph(len(self.coords))  # create initial empty graph

        # Add nodes to networkx
        for idx, coord in enumerate(self.coords):
            for k, v in {'label': idx,
                 'physics': False,
                 'x': coord['x'] * 1.4,
                 'y': coord['y'] * 1.4,
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

            # print("generated Network")
            self.nx_graph_default = self.nx_graph.copy()


    def load_solution(self, iteration):        
        '''
            Update and plot solution
        '''
        # Reset graph
        self.nx_graph = self.nx_graph_default.copy()
        if self.iterations[iteration]['path'] == []:
            return 

        label = ''
        for node1, node2 in self.iterations[iteration]['path']:
            if self.hide_weight == False and self.distance_matrix[node1][node2] != 0:
                label = f'{int(self.distance_matrix[node1][node2])}'

            # If the edge is self loop, then the node is a initial one
            if node1 == node2:
                for k, v in {'label':node1,
                    'physics': False,
                    'x': self.coords[node1]['x'] * 1.4,
                    'y': self.coords[node1]['y'] * 1.4,
                    'size': 2,
                    'shape': 'circle' if self.circle_bool else 'dot',
                    'color': 'rgb(139,0,0)',
                    }.items():

                    self.nx_graph.nodes[node1][k] = v
            else:
                self.nx_graph.add_edge(node1, node2, width=3, color='rgb(139,0,0)', label=label)


    @st.cache
    def calling_solver(self, series_pick, solver):
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
        elif self.solver == "2opt":
            os.system("./main.py visualization -i {0} -s {1} -I nn".format(self.series_pick, self.solver))
            self.iterations = self.read_tracking(trackingPath + self.series_pick + '_' + self.solver + '.txt')
        elif self.solver == "chris":
            os.system("./main.py visualization -i {0} -s {1}".format(self.series_pick, self.solver))
            self.iterations = self.read_tracking(trackingPath + self.series_pick + '_' + self.solver + '.txt')

        return [True, '']


    def render_instance(self, render_graph_html, iteration, circle_bool, hide_edges_bool, hide_weight, h = 500, w = 750):
        """
            Render a networkx graph in screen
        """
        # print("Changed to: ", iteration)
        self.iteration = iteration

        # If some propriety change, update value and reload the Networx Graph
        if self.circle_bool != circle_bool or self.hide_edges_bool != hide_edges_bool or self.hide_weight != hide_weight:
            self.circle_bool        = circle_bool
            self.hide_edges_bool    = hide_edges_bool
            self.hide_weight        = hide_weight
            self.load_nx_graph()

        self.load_solution(iteration)

        # Translate to pyvis network
        nt = Network(f'{h}px', f'{w}px',
                    font_color='white')
        nt.from_nx(self.nx_graph)
        nt.toggle_physics(False)
        path = f'network.html'
        nt.save_graph(path)

        HtmlFile = open(path, 'r')  # , encoding='utf-8')
        source_code = HtmlFile.read()

        # Clean screen before plot
        if render_graph_html != None:
            render_graph_html.empty()

        render_html = components.html(source_code, height=h * 1.1, width=w * 1.1)
        
        return render_html


    def fromstring(self, path_string):
        '''
            This function parse the matrix in string to a array matrix in python
        '''
        simbol_set = ['[', ']', ',']
        arr_list = list(path_string)

        matrix = []
        row = []
        num_compose = ''
        i = 0
        while(i < len(arr_list)):
            
            if(len(row) == 2):
                matrix.append(row)
                row = []

            while(i < len(arr_list) and arr_list[i] in simbol_set):
                i += 1

            while(i < len(arr_list) and (arr_list[i] not in simbol_set)):
                num_compose += arr_list[i]
                i += 1

            if(num_compose != ''):
                row.append(int(num_compose))
                num_compose = ''

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
            lines = file.readlines()
            file.close()
        except:
            print("The input file does not exist.")
            return 0
            
        # For each iteration
        for it, iteration in enumerate(lines):
            
            # Read the haeder
            if it == 0:
                continue
         
            id_iteration, path_string, time_elapsed, objective_value = iteration.split('_')
            objective_value = objective_value[:len(objective_value)-1]
            iterations[int(id_iteration)] = { 'path': self.fromstring(path_string), 'time_elapsed': time_elapsed, 'objective_value': objective_value }
         
        return iterations


