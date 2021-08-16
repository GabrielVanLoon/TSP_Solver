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

@st.cache(allow_output_mutation=True)
def load_class_simulador(series_pick, option_alg):
    return Simulator(series_pick=series_pick, solver=option_alg)

@st.cache()
def solve_class_simulador(series_pick, option_alg):
    print("Solving serie: {0} with alg: {1}".format(series_pick, option_alg))
    return simulator.solving()

###############################################
### Choosing params 
###############################################
st.sidebar.markdown('# Configuração')

# for selecting series
# series_pick = st.sidebar.selectbox('Select series:',
#                                    list(dict({'Initial': "Initial",}).values()),
#                                    key='series', index=1)
series_pick = st.sidebar.selectbox('Caso Teste:', ('orion15', 'Enviar um caso teste...'), index = 1)
option_alg = st.sidebar.selectbox('Algoritmo 1: ', ('NN (Nearest Neighbor)','Christofides'))

###############################################
# Init simulation
###############################################
st.markdown(
    '''### Simulador TSP 
Selecione um algoritmo e visualize como ele performa solucionando o problema do Traveling Salesman Problem (TSP).\n
Clique e arraste os vértices para melhor visualização.
''')
simulator = load_class_simulador(series_pick, option_alg)

################################################
#### Render CHART ###
################################################
_, sidebar_col2, _ = st.sidebar.columns(3)
_, main_col2, _ = st.columns(3)

if series_pick == 'Enviar um caso teste...':
    print('TODO')
else:
    status_solver, msg = solve_class_simulador(series_pick, option_alg)

if sidebar_col2.button('Start'):
    gif_runner = main_col2.image('./images/icons/spinner.gif')
    
    if series_pick == 'Enviar um caso teste...':
        status_solver, msg = False, 'Escolha um teste disponível.'
        print('TODO')
    else:
        status_solver, msg = simulator.solving()
    
    if status_solver != True:
        html_error_msg = label_generator.error(msg)
        label_error = st.markdown(html_error_msg, unsafe_allow_html=True)

    gif_runner.empty()
  
################################################
#### INTERACTIONS CHART
################################################

# Define options in sidebar
if status_solver == True:
    st.sidebar.markdown('## OPÇÕES')
    id_iteration = options(st, len(simulator.iterations))
    st.write(id_iteration)
    simulator.render_instance(id_iteration)

################################################
#### Footer ###
################################################

st.markdown(
    '''#### Descrição
    visualize como diferentes soluções agem ao buscar um caminho para o problema do Caixeiro Viajante.
''')


###############
#### ABOUT ####
###############

st.sidebar.markdown('''
## ABOUT
Code: [source]()\n
Author: [profile]()
Tools: [Streamlit](https://streamlit.io/), [Altair](https://altair-viz.github.io/), [Networkx](https://networkx.org/) & [Pyvis](https://pyvis.readthedocs.io/en/latest/)
''')