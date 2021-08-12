import numpy as np
import matplotlib.pyplot as plt; plt.ion()
import networkx
import netgraph # pip install netgraph

# Construct sparse, directed, weighted graph
total_nodes = 20
weights = np.random.rand(total_nodes, total_nodes)
connection_probability = 0.1
is_connected = np.random.rand(total_nodes, total_nodes) <= connection_probability
graph = np.zeros((total_nodes, total_nodes))
graph[is_connected] = weights[is_connected]

# construct a networkx graph
g = networkx.from_numpy_array(graph, networkx.DiGraph)

# decide on a layout
pos = networkx.layout.spring_layout(g)

# Create an interactive plot.
# NOTE: you must retain a reference to the object instance!
# Otherwise the whole thing will be garbage collected after the initial draw
# and you won't be able to move the plot elements around.
plot_instance = netgraph.InteractiveGraph(graph, node_positions=pos)

######## drag nodes around #########

# To access the new node positions:
node_positions = plot_instance.node_positions

plt.show()