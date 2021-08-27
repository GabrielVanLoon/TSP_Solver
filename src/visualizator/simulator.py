from solver import Solver
import streamlit as st
import streamlit.components.v1 as components

class Simulator:

    def __init__(self, series_pick, solver, initial_node = 0, initial_solution = []): 
        self.main_solver    = Solver(series_pick, solver)
        self.slave_solver   = None 
        return

    @st.cache
    def select_slave_solver(self, series_pick, solver):
        self.slave_solver = Solver(series_pick, solver)
        return


    def next_iteration(self, method):
        '''
            Pass the solver to the next iteration if possible
        '''
        return


    def compare_solution(self):
        if self.main_solver == None or self.slave_solver == None:
            return 
        return 
    