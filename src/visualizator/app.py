import streamlit as st
import streamlit.components.v1 as components

import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import time

from solver import Solver
from simulator import Simulator
from components.buttons import Button
from side_options import options

# Distancia dada ou não 
# normalizar o tempo
# input : cada frame corresponde à

##############################################
### Style
##############################################
st.set_page_config(page_title='Simulator TSP')

st.markdown(""" <style> 
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;} 
        </style> """, unsafe_allow_html=True)

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

label_generator = Button()
status_solver = False
render_graph_html = None
render_graph2_html = None

h = 500
w = 500

@st.cache(allow_output_mutation=True)
def simulador_start(series_pick, option_alg):
    print("Starting simulation...")
    return Simulator(series_pick=series_pick, solver=option_alg)


@st.cache(allow_output_mutation=True)
def simulador_select_solver(series_pick, option_alg):
    print("Starting second simulation...")
    simulator.select_slave_solver(series_pick, option_alg)


@st.cache()
def simulador_main_solve(series_pick, option_alg):
    print("Solving Main Solver serie: {0} with alg: {1}".format(series_pick, option_alg))
    return simulator.main_solver.calling_solver(series_pick, option_alg)


@st.cache()
def simulador_slave_solve(series_pick, option_alg):
    print("Solving Slave Solver serie: {0} with alg: {1}".format(series_pick, option_alg))
    return simulator.slave_solver.calling_solver(series_pick, option_alg)


###############################################
### Choosing params 
###############################################
st.sidebar.markdown('# Configuração')

# for selecting series
# series_pick = st.sidebar.selectbox('Select series:',
#                                    list(dict({'Initial': "Initial",}).values()),
#                                    key='series', index=1)
algoritmos = {'NN (Nearest Neighbor)' : 'Construtivo', 
              'Two Opt'               : 'Incremental', 
              'Christofides'          : 'Construtivo'}

series_pick = st.sidebar.selectbox('Caso Teste:', ('orion15', 'libra6', 'Enviar um caso teste...'), index = 1)
option_alg = st.sidebar.selectbox('Algoritmo 1: ', list([alg for alg, tipo in algoritmos.items()]))
option_alg2 = st.sidebar.selectbox('Algoritmo 2: ', ['Nenhum'] + list([alg for alg, tipo in algoritmos.items() if alg != option_alg and tipo == algoritmos[option_alg]]))

###############################################
# Init simulation
###############################################
st.markdown(
    '''### Simulador TSP 
Selecione um algoritmo e visualize como ele performa solucionando o problema do Traveling Salesman Problem (TSP).\n
''')
simulator = simulador_start(series_pick, option_alg)

if option_alg2 != "Nenhum":
    simulador_select_solver(series_pick, option_alg2)

################################################
#### Render CHART ###
################################################
sidebar_col1, sidebar_col2, sidebar_col3 = st.sidebar.columns((1, 1, 1))
main_col1, main_col2, main_col3 = st.columns(3)

# On change of series or alg, call solver
if series_pick == 'Enviar um caso teste...':
    print('TODO')
else:
    gif_runner = main_col2.image('./images/icons/spinner.gif')
    status_solver, msg = simulador_main_solve(series_pick, option_alg)

    # Calculate solution for the second option
    if simulator.slave_solver != None and option_alg2 != "Nenhum":
        status_solver2, msg2 = simulador_slave_solve(series_pick, option_alg2)

    if status_solver != True:
        html_error_msg = label_generator.error(msg)
        label_error = st.markdown(html_error_msg, unsafe_allow_html=True)

    gif_runner.empty()

################################################
#### INTERACTIONS CHART
################################################

# Define options in sidebar
if status_solver == True:
    st.sidebar.markdown('##     OPÇÕES')
    
    # Divide the info in two sides
    info_left       = None
    info_right      = None
    slider_left     = None
    slider_right    = None
    slider_ph       = None
    if simulator.slave_solver != None and option_alg2 != "Nenhum":
        info_left, info_right       = st.empty(), st.empty()
        slider_left, slider_right   = st.columns(2)

    else:      
        info_ph     = st.empty()
        slider_ph   = st.sidebar.empty()

    c_left, _, c_right = st.columns([.4, .3, .4])

    value_iteration_left            = 0
    # Update values, if the slave solver exist, the iterations bar must be created
    if simulator.slave_solver != None and option_alg2 != "Nenhum":
        max_left_it                     = len(simulator.main_solver.iterations) - 1
        max_right_it                    = len(simulator.slave_solver.iterations) - 1
        value_iteration_right           = 0
        progress_left                   = slider_left.progress(0)
        progress_right                  = slider_right.progress(0)
        max_iterations                  = max(max_left_it, max_right_it) 
        simulator.main_solver.iteration = value_iteration_left
    else:
        max_left_it                          = len(simulator.main_solver.iterations) - 1
        max_iterations                       = max_left_it
        value_iteration_left                 = slider_ph.slider("Iterações", 0, max_iterations, simulator.main_solver.iteration, 1)
        simulator.main_solver.iteration      = value_iteration_left

    if algoritmos[option_alg] == "Incremental":
        rota_inicial = st.sidebar.selectbox('Rota Inicial: ', list([alg for alg, tipo in algoritmos.items() if tipo == "Construtivo"]) )

    speed_val        = st.sidebar.number_input('Velocidade (S)', min_value=0.5, max_value=10.0, value=1.0, step=0.5)
    circle_bool      = st.sidebar.checkbox('Nós circulares', key='boxb', value=True)
    hide_edges_bool  = st.sidebar.checkbox('Ocultar arestas', key='hedges', value=False)
    hide_weight_bool = st.sidebar.checkbox('Ocultar pesos das arestas', key='hweights', value=False)

    if sidebar_col1.button('Reset'):
        if simulator.slave_solver != None and option_alg2 != "Nenhum":
            simulator.main_solver.iteration  = 0
            simulator.slave_solver.iteration = 0
            slider_left.empty()
            slider_right.empty()
        else:
            simulator.main_solver.iteration  = 0
            slider_ph.empty()
            value_iteration_left = slider_ph.slider("Iterações", 0, max_iterations, 0, 2)

    sidebar_col3.button('Stop')

    # Animate solution per iteration
    if sidebar_col2.button('Start'):

        value_iteration = 1
        
        # If there two solvers, check if the two ended
        if simulator.slave_solver != None and option_alg2 != "Nenhum":
            value_iteration_left  = 1
            value_iteration_right = 1

        # Restart if the actual iteration is the last one
        if value_iteration == max_iterations:
            simulator.main_solver.iteration = value_iteration = 0
        
        for id_iteration in range(value_iteration, max_iterations + 1):  

            # Divide main page in two, in case there are more than one solver          
            with c_left:
                if id_iteration <= max_left_it:
                    value_iteration_left = id_iteration
                    render_graph_html = simulator.main_solver.render_instance(render_graph_html, value_iteration_left, circle_bool, hide_edges_bool, hide_weight_bool, h=h, w=w)

            with c_right:
                if option_alg2 != "Nenhum" and id_iteration <= max_right_it:
                    value_iteration_right = id_iteration
                    render_graph2_html = simulator.slave_solver.render_instance(render_graph2_html, value_iteration_right, circle_bool, hide_edges_bool, hide_weight_bool, h=h, w=w)

            # Update info of the execution
            if simulator.slave_solver != None and option_alg2 != "Nenhum":
                valor_obj = round(float(simulator.main_solver.iterations[value_iteration_left]['objective_value']))
                info_left.info(f'Iteração: {value_iteration_left} - Custo: {valor_obj}')
                progress_left.progress(value_iteration_left/max_left_it)
                
                valor_obj = round(float(simulator.slave_solver.iterations[value_iteration_right]['objective_value']))
                info_right.info(f'Iteração: {value_iteration_right} - Custo: {valor_obj}')
                progress_right.progress(value_iteration_right/max_right_it)
            else:
                value_iteration = slider_ph.slider("Iterações", 0, max_iterations, value_iteration + 1, 3)
                valor_obj = round(float(simulator.main_solver.iterations[value_iteration]['objective_value']))
                time_elapesed = round(float(simulator.main_solver.iterations[value_iteration]['time_elapesed']))
                info_ph.info(f'Iteração: {value_iteration} - Tempo: {time_elapesed} s - Custo: {valor_obj}')
            
            time.sleep(1.0/speed_val)
    else:
        # Render graph
        with c_left:
            if simulator.main_solver != None:
                simulator.main_solver.render_instance(render_graph_html, value_iteration_left, circle_bool, hide_edges_bool, hide_weight_bool, h=h, w=w)

        with c_right:
            if option_alg2 != "Nenhum" and simulator.slave_solver != None:
                simulator.slave_solver.render_instance(render_graph2_html, value_iteration_right, circle_bool, hide_edges_bool, hide_weight_bool, h=h, w=w)


if simulator.slave_solver != None and option_alg2 != "Nenhum":
    # value_iteration_left    = slider_left.slider("Iterações", 0, len(simulator.main_solver.iterations) - 1, simulator.main_solver.iteration, 3)
    valor_obj               = round(float(simulator.main_solver.iterations[value_iteration_left]['objective_value']))
    info_left.info(f'Algoritmo: {option_alg} - Iteração: {value_iteration_left} - Custo: {valor_obj}')
    progress_left.progress(value_iteration_left/max_left_it)

    # value_iteration_right   = slider_right.slider("Iterações", 0, len(simulator.slave_solver.iterations) - 1, simulator.slave_solver.iteration, 3)
    valor_obj               = round(float(simulator.slave_solver.iterations[value_iteration_right]['objective_value']))
    info_right.info(f'Algoritmo: {option_alg2} - Iteração: {value_iteration_right} - Custo: {valor_obj}')
    progress_right.progress(value_iteration_right/max_right_it)
else:
    valor_obj               = round(float(simulator.main_solver.iterations[value_iteration_left]['objective_value']))
    time_elapesed           = round(float(simulator.main_solver.iterations[value_iteration_left]['time_elapsed']) * 1000, 3)
    info_ph.info(f'Iteração: {value_iteration_left} - Tempo: {str(time_elapesed)} s - Custo: {valor_obj}')

################################################
#### Footer ###
################################################

st.markdown(
    '''
    Clique e arraste os vértices para melhor visualização.
''', unsafe_allow_html=True)


###############
#### ABOUT ####
###############

st.sidebar.markdown('''
## Descrição
Visualize como diferentes soluções agem ao buscar um caminho para o problema do Caixeiro Viajante.\n
Código: [fonte](https://github.com/Math-O5/tsp-solver)\n
Ferramentas: [Streamlit](https://streamlit.io/), [Altair](https://altair-viz.github.io/), [Networkx](https://networkx.org/) & [Pyvis](https://pyvis.readthedocs.io/en/latest/)
''')