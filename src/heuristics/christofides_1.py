
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy as np
from munkres import Munkres
import networkx as nx
import copy
import itertools
from operator import itemgetter
import time

class Christofides:
    def __init__(self, dist_matrix, tracking=False):
        '''
        Classe construtora a qual comeca inicializando
        a matriz de distancia, o custo (infinito) e o caminho (ainda vazio)

        Parametros
        ----------
            dist_matrix : np.array
                Matriz de distancias

            tracking    : bool 
                Enable output though iterations
        '''
        self.dist_matrix        = dist_matrix
        self.number_of_nodes    = len(dist_matrix)
        self.cost               = np.inf
        self.path               = []
        self.final_path         = []
        
        self.tracking           = tracking
        self.iterations         = {}                    # id, solution, objective_value, time_elapsed
        self.iterator           = 0
        self.status             = None
        self.objective_value    = 0


    def _csr_gen_triples(self, A):
        """Converts a SciPy sparse matrix in **Compressed Sparse Row** format to
        an iterable of weighted edge triples.
        """
        graph = nx.Graph()
        nrows = A.shape[0]
        data, indices, indptr = A.data, A.indices, A.indptr
        for i in range(nrows):
            for j in range(indptr[i], indptr[i+1]):
                graph.add_edge(i,indices[j], weight = data[j])   
        return graph.edges(data = 'weight')


    def _odd_vertices_of_MST(self, MST):
        """Returns the vertices having Odd degree in the Minimum Spanning Tree(MST).
        """
        odd_vertices = [0 for i in range(self.number_of_nodes)]
        for u,v,d in MST:
            odd_vertices[u] = odd_vertices[u] + 1
            odd_vertices[v] = odd_vertices[v] + 1
        odd_vertices = [vertex for vertex, degree in enumerate(odd_vertices) if degree % 2 == 1]
        return odd_vertices


    def min_Munkres(self, bipartite_graphs):
        """Implements the Hungarian problem or the Assignment problem to
        find Minimum Cost Perfect Matching(MCPM).
        """
        m = Munkres()
        minimum = np.inf
        for index,bipartite_graph in enumerate(bipartite_graphs[0]):
            Munkres_indexes = m.compute(bipartite_graph)
            cost = self.Munkres_cost(Munkres_indexes, bipartite_graph)
            if cost < minimum:
                minimum = cost
                min_index = index
                min_Munkres_indexes = Munkres_indexes
        Munkres_indexes = [[] for i in range(len(min_Munkres_indexes))]
        for index,vertex_set in enumerate(min_Munkres_indexes):
            Munkres_indexes[index].append(bipartite_graphs[1][min_index][0][vertex_set[0]])
            Munkres_indexes[index].append(bipartite_graphs[1][min_index][1][vertex_set[1]])
        return Munkres_indexes


    def Munkres_cost(self, indexes, bipartite_graph):
        """Returns cost of the edges in Munkres_indexes
        """
        cost = 0
        for index in indexes:
            cost = cost + bipartite_graph[index[0]][index[1]]
        return cost


    def bipartite_Graph(self, bipartite_set, odd_vertices):
        """
        """
        bipartite_graphs = []
        vertex_sets = []
        for vertex_set1 in bipartite_set:
            vertex_set1 = list(sorted(vertex_set1))
            vertex_set2 = []
            for vertex in odd_vertices:
                if vertex not in vertex_set1:
                    vertex_set2.append(vertex)
            matrix = [[np.inf for j in range(len(vertex_set2))] for i in range(len(vertex_set1))]
            for i in range(len(vertex_set1)):
                for j in range(len(vertex_set2)):
                    if vertex_set1[i] < vertex_set2[j]:
                        matrix[i][j] = self.dist_matrix[vertex_set1[i]][vertex_set2[j]]
                    else:
                        matrix[i][j] = self.dist_matrix[vertex_set2[j]][vertex_set1[i]]
            bipartite_graphs.append(matrix)
            vertex_sets.append([vertex_set1,vertex_set2])
        return [bipartite_graphs, vertex_sets]


    def create_Multigraph(self, MST, indexes, odd_vertices):
        """Creates a MultiGraph consisting of vertices of both
        MST and MCPM.
        """
        multigraph = nx.MultiGraph()
        for u,v,d in MST:
            multigraph.add_edge(u,v,weight=d)
        for pair in indexes:
            multigraph.add_edge(pair[0],pair[1],weight=self.dist_matrix[pair[0]][pair[1]])
        return multigraph


    def shortcut_Euler_Tour(self, tour):
        """Find's the shortcut of the Euler Tour to obtain the Approximation.
        """
        Tour = []
        for vertex in tour:
            if vertex not in Tour:
                Tour.append(vertex)
        Tour.append(tour[0])
        return Tour


    def resolve_final_path(self):
        """Returns Cost of Tour.
        """
        Travel_Cost = 0
        self.final_path = []
        print(self.path)
        christofides_tour = self.path[0:len(self.path)]
        previous_vertex = christofides_tour[-1]

        for current_vertex in christofides_tour:
            if previous_vertex > current_vertex:
                Travel_Cost = Travel_Cost + self.dist_matrix[current_vertex][previous_vertex]
            else:
                Travel_Cost = Travel_Cost + self.dist_matrix[previous_vertex][current_vertex]

            self.final_path.append([previous_vertex, current_vertex]) 
            self.objective_value = Travel_Cost

            previous_vertex = current_vertex
            

    def format_time(self, time1, time2):
        # return round((time2 - time1), 2)
        return time2 - time1


    def extract_mst(self, MST,):
        edges = []
        total_cost  = 0
        for u, v, cost in MST:
            edges.append([u, v])
            total_cost += cost
    
        # Save to the instance
        self.final_path = edges
        self.objective_value = total_cost


    def solve(self):
        """Returns an Approximation for TSP using Christofide's algorithm by
        directing several functions.
        """
        self.iterator = 0
        if self.tracking:
            self.iterations[self.iterator] = {'path': [], 'time_elapsed': 0.0, 'objective_value': 0.0}
            self.iterator += 1 

        time1 = time.time()
        MST                 = self._csr_gen_triples(minimum_spanning_tree(csr_matrix(self.dist_matrix)))
        time2 = time.time()

        if self.tracking:
            # Extract MST
            self.extract_mst(MST)
            self.iterations[self.iterator] = {'path': self.final_path.copy(), 'time_elapsed': self.format_time(time1, time2), 'objective_value': self.objective_value}
            self.iterator += 1 
        
        time1 = time.time()
        odd_vertices        = self._odd_vertices_of_MST(MST)
        time2 = time.time()

        if self.tracking:
            # Paint odd vertices
            for node in odd_vertices:
                self.final_path.append([node, node])

            self.iterations[self.iterator] = {'path': self.final_path.copy(), 'time_elapsed': self.format_time(time1, time2), 'objective_value': self.objective_value}
            self.iterator += 1 

        time1 = time.time()
        bipartite_set       = [set(i) for i in itertools.combinations(set(odd_vertices), len(odd_vertices)//2)]
        bipartite_graphs    = self.bipartite_Graph(bipartite_set, odd_vertices)
        indexes             = self.min_Munkres(bipartite_graphs)
        time2 = time.time()

        if self.tracking:
            # Add edges from the macthing vertices
            for index in indexes:
                self.final_path.append(index)
                self.objective_value += self.dist_matrix[index[0]][index[1]]

            self.iterations[self.iterator] = {'path': self.final_path.copy(), 'time_elapsed': self.format_time(time1, time2), 'objective_value': self.objective_value}
            self.iterator += 1 

        time1 = time.time()
        multigraph          = self.create_Multigraph(MST, indexes, odd_vertices)
        multiGraph          = copy.deepcopy(multigraph)
        euler_tour          = [u for u, v in nx.eulerian_circuit(multigraph)]
        time2 = time.time()

        if self.tracking:
            # Add edges from the macthing vertices
            self.path = euler_tour 
            self.resolve_final_path()

            self.iterations[self.iterator] = {'path': self.final_path.copy(), 'time_elapsed': self.format_time(time1, time2), 'objective_value': self.objective_value}
            self.iterator += 1 

        time1 = time.time()
        Christofides_Solution   = self.shortcut_Euler_Tour(euler_tour)
        time2 = time.time()
        
        self.path               = Christofides_Solution

        if self.tracking:
            # Add edges from the macthing vertices
            self.path = Christofides_Solution 
            self.resolve_final_path()

            self.iterations[self.iterator] = {'path': self.final_path.copy(), 'time_elapsed': self.format_time(time1, time2), 'objective_value': self.objective_value}
            self.iterator += 1 
            
# if __name__ == "__main__":
# 	print('Testing...')
# 	start = time.time()
# 	dist_matrix =[[0,45,65,15],
#                         [0,0,56,12],
#                         [0,0,0,89],
#                         [0,0,0,0]]
# 	Approximation =  compute(dist_matrix)
# 	end = time.time()-start
# 	print('Computation Successful...')
# 	print('Distance Matrix:\n')
# 	print(dist_matrix)
# 	print('\n1.5 Approximation of TSP (Christofide\'s algorithm):\n', Approximation['Christofides_Solution'])
# 	print('Travel Cost:', Approximation['Travel_Cost'])
# 	print('Computation Time:', end)
# 	print ('')

# {'Christofides_Solution': [0, 1, 9, 10, 11, 12, 13, 14, 8, 6, 5, 7, 4, 3, 2, 0], 
# 'Travel_Cost': 1396.0, 
# 'MST': EdgeDataView([(0, 2, 133.0), (0, 1, 140.0), (2, 3, 23.0), (3, 4, 23.0), (4, 8, 113.0), (8, 7, 69.0), (8, 14, 133.0), (5, 6, 42.0), (5, 7, 89.0), (9, 10, 35.0), (10, 11, 32.0), (11, 12, 25.0), (12, 13, 47.0), (13, 14, 29.0)]), 
# 'Odd_Vertices': [1, 6, 8, 9], 
# 'Indexes': [[1, 9], [8, 6]], 
# 'Multigraph': MultiEdgeDataView([(0, 2, 133.0), (0, 1, 140.0), (2, 3, 23.0), (1, 9, 323.0), (3, 4, 23.0), (4, 8, 113.0), (8, 7, 69.0), (8, 14, 133.0), (8, 6, 156.0), (7, 5, 89.0), (14, 13, 29.0), (5, 6, 42.0), (9, 10, 35.0), (10, 11, 32.0), (11, 12, 25.0), (12, 13, 47.0)]), 
# 'Euler_Tour': [0, 1, 9, 10, 11, 12, 13, 14, 8, 6, 5, 7, 8, 4, 3, 2]}