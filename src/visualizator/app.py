import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from simulator import Simulator
import time

# Distancia dada ou não 
# normalizar o tempo
# input : cada frame corresponde à

#####################################
# Style
#####################################
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

#####################################
# Choosing params
#####################################
st.sidebar.markdown('# Choose your params')

# for selecting series
# series_pick = st.sidebar.selectbox('Select series:',
#                                    list(dict({'Initial': "Initial",}).values()),
#                                    key='series', index=1)
series_pick = st.sidebar.selectbox('Select series:', ('Initial', 'Initial', 'Choose your file...'), index = 1)
option_alg = st.sidebar.selectbox('Select algorithm: ',('NN (Nearest Neighbor)','Christofides'))

#####################################
# Init simulation
#####################################
st.markdown(
    '''#### Simulator TSP
Select the algorithm and visualize\n
Click and drag nodes to rearrange the network.
''')
simulator = Simulator()

###########################
#### INTERACTIONS CHART ###
###########################

# define options in sidebar
st.sidebar.markdown('## NETWORK OPTIONS')
physics_bool = st.sidebar.checkbox(
    'Add physics engine', key='phys', value=False)
box_bool = st.sidebar.checkbox('Make nodes boxes', key='boxb', value=True)
col_bool = st.sidebar.checkbox('Random colors', key='colb', value=False)

interactions = st.sidebar.slider(
    label="Itaração",
    min_value=0,
    max_value=4,
    step=1,
    value=0)

simulator.render_instance("Initial")

HtmlFile = open("initial.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 500*1.1,width=750*1.1)

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(1.5)

st.markdown(
    '''#### Description
yadda, yadda
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