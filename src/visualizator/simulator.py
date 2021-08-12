  
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st

class Simulator:

    def __init__(self, distance_matrix = [], initial_node = 0, initial_solution = []):
        self.distance_matrix = distance_matrix
        self.n_nodes = len(distance_matrix)
        self.iterations = {} # id, edges, objective_value, time_elapsed

        # Initial Configurations
        self.initial_node = initial_node
        self.initial_solution = initial_solution

        # Animations
        self.iteration = 0

    def render_instance(self, instance_name):
        # Generate initial network
        G = nx.karate_club_graph()
        instance =  Network(height="500px", width="750px", font_color="black")
        instance.from_nx(G)     
        instance.toggle_physics(False)
        instance.show('initial.html')