import csv

def tracking_csv(my_solver, coord_filename, route_filename):
    '''
    Cria um arquivo csv de rotas. O cabecalho do arquivo criado sera 
    x_i, y_i, x_j e y_j sendo i a coordenada de saida e j a coordenada
    de entrada

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
    with open(route_filename, mode='w') as txt_file:
        txt_file.write('id, path, time_elapesed\n')
        for it, iteration in enumerate(my_solver.iterations.values()):
            # Extract from dict
            path = iteration['path']
            time_elapsed = iteration['time_elapsed']
            objective_value = iteration['objective_value']

            # Convert values into string
            id_string = f'{it}'
            path_string = '['
            time_string = f'{time_elapsed}' 
            objective_value_string = f'{objective_value}'
    
            for i, j in path:
                path_string += f'[{int(i)},{int(j)}]'
            path_string += ']'

            # Write to the file text
            txt_file.write('-'.join([id_string, path_string, time_string, objective_value_string]))
            txt_file.write('\n')



            
