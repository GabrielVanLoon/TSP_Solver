import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from simulator import Simulator
import time

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

@st.cache(allow_output_mutation=True)
def load_class_simulador(series_pick, option_alg):
    print("Startinf simulation...")
    return Simulator(series_pick=series_pick, solver=option_alg)

@st.cache()
def solve_class_simulador(series_pick, option_alg):
    print("Solving serie: {0} with alg: {1}".format(series_pick, option_alg))
    return simulator.calling_solver(series_pick, option_alg)

###############################################
### Choosing params 
###############################################
st.sidebar.markdown('# Configuração')

# for selecting series
# series_pick = st.sidebar.selectbox('Select series:',
#                                    list(dict({'Initial': "Initial",}).values()),
#                                    key='series', index=1)
series_pick = st.sidebar.selectbox('Caso Teste:', ('orion15', 'libra6', 'Enviar um caso teste...'), index = 1)
option_alg = st.sidebar.selectbox('Algoritmo 1: ', ('NN (Nearest Neighbor)', 'Two Opt', 'Christofides'))

###############################################
# Init simulation
###############################################
# st.markdown(
#     '''### Simulador TSP 
# Selecione um algoritmo e visualize como ele performa solucionando o problema do Traveling Salesman Problem (TSP).\n
# Clique e arraste os vértices para melhor visualização.
# ''')
simulator = load_class_simulador(series_pick, option_alg)

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
    status_solver, msg = solve_class_simulador(series_pick, option_alg)

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
    
    slider_ph = st.sidebar.empty()
    info_ph = st.empty()

    max_iterations = len(simulator.iterations) - 1
    value_iteration = slider_ph.slider("Iterações", 0, max_iterations, simulator.iteration, 1)
    simulator.iteration = value_iteration
    speed_val = st.sidebar.number_input('Velocidade (S)', min_value=0.5, max_value=10.0, value=1.0, step=0.5)

    circle_bool = st.sidebar.checkbox('Nós circulares', key='boxb', value=True)
    hide_edges_bool = st.sidebar.checkbox('Ocultar arestas', key='hedges', value=False)
    hide_weight_bool = st.sidebar.checkbox('Ocultar pesos das arestas', key='hweights', value=False)

    if sidebar_col1.button('Reset'):
        simulator.iteration = 0
        slider_ph.empty()
        value_iteration = slider_ph.slider("Iterações", 0, max_iterations, 0, 2)

    sidebar_col3.button('Stop')

    if sidebar_col2.button('Start'):

        if value_iteration == max_iterations:
            simulator.iteration = value_iteration = 0

        for id_iteration in range(value_iteration, max_iterations):
            # Clean screen before plot
            if render_graph_html != None:
                render_graph_html.empty()

            render_graph_html = simulator.render_instance(id_iteration, circle_bool, hide_edges_bool, hide_weight_bool)

            value_iteration = slider_ph.slider("Iterações", 0, max_iterations, value_iteration + 1, 3)
            valor_obj = round(float(simulator.iterations[value_iteration]['objective_value']))
            info_ph.info(f'Iteração: {value_iteration} - Custo: {valor_obj}')
            time.sleep(1.0/speed_val)

    if render_graph_html != None:
        render_graph_html.empty()
    render_graph_html = simulator.render_instance(value_iteration, circle_bool, hide_edges_bool, hide_weight_bool, h=500, w=750)
    render_graph_html = simulator.render_instance(value_iteration, circle_bool, hide_edges_bool, hide_weight_bool, h=500, w=750)

valor_obj = round(float(simulator.iterations[value_iteration]['objective_value']))
info_ph.info(f'Iteração: {value_iteration} - Custo: {valor_obj}')

# main_col2.write(int(simulator.objective_value))

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