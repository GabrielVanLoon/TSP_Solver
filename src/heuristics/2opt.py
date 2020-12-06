import csv
import time
import numpy as np
from math import inf

"""
    Execucao com a biblioteca py2opt

    qatar194
    200 iterations
    909 sec
    9608.0 length
    ['1', '2', '3', '5', '9', '10', '12', '15', '19', '30', '32', '31', '27', '37', '39', '34', '40', '43', '48', '46', '41', '38', '35', '44', '42', '50', '49', '55', '54', '52', '53', '56', '58', '47', '51', '61', '66', '67', '73', '68', '64', '70', '77', '84', '100', '97', '96', '93', '95', '92', '81', '79', '83', '88', '91', '78', '75', '72', '74', '69', '60', '57', '45', '29', '22', '28', '33', '18', '21', '24', '26', '17', '14', '11', '7', '4', '6', '8', '16', '13', '23', '25', '71', '76', '80', '87', '102', '103', '106', '105', '107', '108', '110', '112', '115', '116', '117', '121', '120', '123', '124', '128', '133', '129', '135', '143', '160', '166', '162', '159', '165', '168', '177', '181', '178', '170', '167', '171', '185', '180', '193', '188', '191', '192', '189', '184', '187', '190', '194', '182', '176', '172', '179', '186', '183', '175', '173', '174', '169', '164', '163', '161', '156', '149', '146', '142', '145', '140', '137', '134', '132', '130', '127', '125', '126', '138', '139', '144', '150', '154', '157', '153', '152', '141', '147', '158', '151', '155', '148', '136', '131', '118', '122', '119', '113', '109', '114', '111', '104', '101', '99', '89', '90', '94', '98', '86', '85', '65', '20', '63', '36', '59', '62', '82']
    
    uruguay734
    5 iterations
    1143 sec
    86323.0 length
    ['1', '3', '6', '11', '2', '7', '5', '4', '8', '10', '15', '12', '13', '9', '14', '23', '20', '29', '31', '38', '51', '43', '39', '40', '34', '28', '26', '24', '17', '19', '21', '25', '22', '18', '16', '27', '47', '46', '36', '45', '77', '84', '85', '79', '80', '81', '86', '91', '115', '127', '93', '110', '109', '118', '133', '171', '170', '187', '196', '184', '215', '192', '181', '182', '213', '209', '229', '240', '248', '271', '242', '257', '247', '256', '246', '281', '289', '326', '314', '357', '379', '421', '402', '412', '375', '348', '337', '325', '322', '338', '353', '374', '384', '387', '372', '401', '395', '424', '447', '446', '451', '448', '439', '438', '411', '381', '352', '331', '292', '295', '317', '313', '296', '270', '263', '262', '269', '237', '212', '195', '191', '169', '165', '162', '180', '190', '208', '253', '245', '266', '294', '306', '312', '343', '365', '390', '392', '368', '364', '340', '336', '330', '332', '301', '305', '280', '265', '261', '252', '236', '234', '205', '151', '140', '134', '132', '125', '143', '147', '126', '120', '100', '121', '124', '123', '105', '76', '68', '58', '67', '75', '74', '73', '72', '63', '54', '53', '50', '44', '41', '56', '66', '95', '83', '69', '98', '92', '60', '55', '71', '65', '42', '49', '62', '70', '89', '90', '104', '113', '108', '112', '107', '119', '131', '137', '142', '157', '156', '160', '161', '163', '168', '179', '167', '178', '176', '159', '150', '200', '186', '199', '207', '230', '233', '235', '251', '243', '239', '224', '220', '227', '231', '244', '274', '267', '268', '272', '277', '284', '300', '321', '324', '316', '298', '291', '310', '323', '334', '342', '351', '360', '329', '328', '339', '345', '346', '335', '371', '400', '378', '370', '369', '386', '414', '413', '423', '432', '434', '450', '435', '442', '418', '408', '410', '416', '422', '436', '458', '475', '478', '497', '486', '507', '529', '510', '506', '521', '525', '491', '484', '457', '437', '431', '433', '430', '417', '406', '405', '383', '380', '377', '376', '389', '409', '420', '425', '445', '428', '429', '441', '477', '505', '487', '502', '568', '596', '569', '603', '641', '582', '597', '583', '550', '561', '587', '598', '626', '648', '636', '635', '639', '653', '656', '670', '649', '647', '620', '638', '625', '574', '563', '570', '555', '538', '530', '533', '534', '552', '541', '511', '503', '488', '492', '489', '514', '459', '453', '419', '426', '443', '462', '454', '465', '470', '479', '493', '508', '499', '498', '535', '537', '523', '536', '526', '517', '512', '504', '490', '500', '494', '485', '480', '476', '460', '455', '449', '463', '473', '472', '483', '481', '501', '515', '520', '522', '519', '513', '509', '518', '527', '544', '539', '543', '551', '559', '558', '591', '614', '623', '633', '632', '622', '618', '613', '585', '576', '572', '630', '602', '567', '590', '621', '612', '617', '589', '580', '575', '579', '584', '611', '601', '600', '578', '557', '560', '556', '542', '571', '562', '548', '564', '588', '586', '577', '581', '607', '637', '642', '650', '664', '665', '671', '659', '663', '610', '604', '616', '624', '640', '643', '655', '658', '687', '691', '697', '715', '721', '720', '719', '731', '730', '728', '729', '718', '710', '713', '714', '717', '727', '732', '733', '726', '725', '706', '707', '702', '703', '700', '698', '711', '722', '716', '699', '690', '686', '681', '674', '682', '701', '704', '708', '709', '705', '696', '695', '688', '685', '678', '672', '666', '651', '644', '645', '646', '631', '619', '615', '606', '599', '592', '573', '609', '605', '629', '628', '627', '654', '660', '669', '657', '677', '673', '662', '689', '680', '684', '676', '675', '694', '724', '693', '683', '679', '668', '661', '692', '723', '734', '712', '652', '634', '667', '595', '594', '608', '593', '549', '545', '546', '565', '553', '540', '531', '516', '524', '566', '532', '547', '554', '528', '496', '474', '469', '471', '444', '404', '394', '391', '399', '427', '456', '466', '482', '495', '467', '468', '461', '464', '452', '440', '415', '403', '388', '393', '385', '362', '349', '361', '358', '318', '302', '297', '293', '285', '278', '221', '210', '204', '214', '228', '222', '216', '254', '250', '249', '279', '309', '319', '327', '315', '303', '282', '275', '258', '283', '286', '290', '287', '299', '311', '288', '259', '255', '273', '260', '232', '238', '217', '211', '218', '223', '225', '219', '194', '183', '202', '201', '198', '206', '197', '193', '185', '188', '172', '158', '164', '144', '136', '152', '148', '177', '173', '145', '141', '129', '128', '116', '102', '101', '94', '87', '78', '64', '32', '30', '33', '35', '37', '48', '52', '57', '59', '61', '88', '111', '114', '97', '82', '96', '99', '103', '106', '122', '138', '146', '174', '153', '154', '149', '135', '117', '130', '139', '155', '166', '175', '189', '203', '226', '241', '264', '276', '304', '344', '341', '355', '373', '359', '363', '347', '333', '356', '320', '308', '307', '350', '354', '367', '366', '382', '398', '407', '397', '396']
"""

class K_opt:
    def __init__(self, dist_matrix):
        self.dist_matrix = dist_matrix
        self.cost  = inf
        self.path  = []

    def initial_solution(self, node_init=0):
        '''
        Calcula a solucao inicial utilizando 
        nearest neighbors

        Parametros
        ----------
            node_init : int
                vertice de inicial
        
        Retorno
        -------
            list(int, ...)
                retorno uma lista com o caminho
        '''
        current_node        = node_init
        self.path           = []
        visited             = np.zeros(len(self.dist_matrix))
        visited[node_init]  = 1
        
        for it in range(len(self.dist_matrix)):
            
            min_dist = inf
            min_viz  = -1

            if it == (len(self.dist_matrix)-1):
                self.path.append(current_node)
            else:
                for viz in range(len(self.dist_matrix)):
                    if (current_node == viz) or (visited[viz] == 1):
                        continue
                    elif self.dist_matrix[current_node][viz] < min_dist:
                        min_dist = self.dist_matrix[current_node][viz]
                        min_viz  = viz
                
                self.path.append(current_node)

                visited[min_viz] = 1
                current_node = min_viz
        
        return self.path
    
    def all_solutions(self):
        '''
        Verifica qual eh o melho
        '''
        
        minimum_dist = inf
        minimum_node = 0

        for i in range(len(self.dist_matrix)):
            opt.initial_solution(node_init=i)
            if minimum_dist > opt.total_cost():
                minimum_dist = opt.total_cost()
                minimum_node = i
        
        if(minimum_node != len(self.dist_matrix)-1):
            opt.initial_solution(node_init=minimum_node)
            minimum_dist = opt.total_cost()

        self.cost = minimum_dist

        return minimum_node, minimum_dist


    def total_cost(self):
        '''
        Calcula o custo total do caminho percorrido

        Retorno
        -------
            int 
                Retorna um valor inteiro com a distancia percorrida
                Caso ainda nao exista self.path, retorna math.inf
        '''

        if self.path == []:
            return inf

        cost = 0
        for node in range(0, len(self.path) - 1):
            cost += self.dist_matrix[self.path[node], self.path[node + 1]]
        cost += self.dist_matrix[self.path[-1], self.path[0]]
        return cost
    
    def edge_cost(self, node1, node2, node3, node4):
        '''
        Calcula o custo da troca das arestas:
        (aresta_atual1 + aresta_atual2) - (aresta_nova1 + aresta_nova2)

        Parametros
        ----------
            node1 : int
                vertice 1 que faz parte da aresta_atual1
            node1 : int
                vertice 2 que faz parte da aresta_atual1
            node3 : int
                vertice 3 que faz parte da aresta_atual2
            node4 : int
                vertice 4 que faz parte da aresta_atual2
        
        Retorno
        -------
            int 
            Retorna o seguinte valor das arestas: (aresta_atual1 + aresta_atual2) - (aresta_nova1 + aresta_nova2)
        '''
        return (self.dist_matrix[node1, node2] + self.dist_matrix[node3, node4]) - (self.dist_matrix[node1, node3] + self.dist_matrix[node2, node4])

    def two_opt(self, iteration=10):
        '''
        Utiliza a heuristica de melhoria de vizinhanca 2-opt
        para minimizar a funcao objetivo. O algoritmo para quando nao 
        eh possivel minimizar a funcao objetivo ou se se atingiu o limite
        de iteracoes

        Parametros
        ----------
            iteration : int
                determina o numero maximo de iteracoes do 2-opt

        Retorno
        -------
            list(int, ...)
                Retorna o melhor caminho encontrado
        '''

        k = 0
        best = self.path
        improved = True
        while improved and k < iteration:
            improved = False
            for i in range(1, len(self.path) - 2):
                for j in range(i + 2,    len(self.path)):
                    if self.edge_cost(best[i-1], best[i], best[j-1], best[j]) > 0:
                        best[i:j] = best[j - 1:i - 1:-1]
                        improved = True
            self.path = best
            k += 1
        return self.path


if __name__=="__main__":

    def load_matrix(file_name='11'):
        with open(f'../../data/distances/{file_name}.txt', 'r') as dist_file:
            cost_matrix = list()
            for line in dist_file:
                cost_matrix.append([int(k) for k in line.strip().split('\t')])
            return np.array(cost_matrix)

    # models = ['djibouti38', 'western_sahara29', 'qatar194', 'uruguay734']
    models = ['djibouti38', 'western_sahara29']

    for m in models:
        time1 = time.time()
        opt   = K_opt(load_matrix(m))
        _, cost = opt.all_solutions()
        time2 = time.time()
        # opt.two_opt() 

        print(m)
        print(cost)
        print('{:.2f} seg.'.format(time2 - time1))


        start_index = opt.path.index(0)
        rotate_path = [] + opt.path[start_index:] + opt.path[:start_index]

        # print(opt.path[start_index:] + opt.path[0:start_index])

        for v in rotate_path:
            print(v, end=" ")


        


# opt = K_opt(load('uruguay734'))
# np.fill_diagonal(opt.dist_matrix, 0)
# print(opt.dist_matrix)
# minimum = inf
# best = 0
# for i in range(734):
#     opt.initial_solution(node_init=i)
#     if minimum > opt.total_cost():
#         minimum = opt.total_cost()
#         best = i

# import time
# time1 = time.time()    
# print(f'Best: {best} and Length: {opt.initial_solution(node_init=best)}')
# print(f'Tempo gasto: {time.time()-time1}', end='\n')
# print(opt.total_cost())
# print(opt.two_opt(iteration=100))
# print(opt.total_cost())
# print(len(opt.path))
# print(len(set(opt.path)))
# print(opt.bfs())