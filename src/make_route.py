import csv

def route_csv(route, coord_filename, route_filename, id_coord_start = 1):
    '''
    Cria um arquivo csv de rotas. O cabecalho do arquivo criado sera 
    x_i, y_i, x_j e y_j sendo i a coordenada de saida e j a coordenada
    de entrada

    Parametros
    ----------
        route : list([(int) i, (int) j])
            lista de rotas. Cada elemento da lista sera composto por dois interos
            sendo uma coordenada de saida e outra de entrada, ex: [[3,0], [0, 4], ...]
        coord_filename : str
            Arquivo csv que tem as coordenadas (id, x, y). Estes arquivos com as coordenadas
            estao na pasta '/data/coord'
        route_filename : str
            Arquivo csv que sera criado para armazenar as rotas
        id_coord_start : int
            Indice da coordenada de inicio
    '''

    coord = dict()

    with open(coord_filename, 'r', encoding='utf-8') as coord_file:
        
        reader = csv.DictReader(coord_file)
        coord = {row['id'] : {'x': row['x'], 'y': row['y']} for row in reader}

    with open(route_filename, 'w') as csv_file:
        
        writer = csv.DictWriter(csv_file, fieldnames=['x_i', 'y_i', 'x_j', 'y_j'])
        writer.writeheader()

        for r in route:
            writer.writerow({'x_i': coord[str(r[0] + id_coord_start)]['x'],
                             'y_i': coord[str(r[0] + id_coord_start)]['y'],
                             'x_j': coord[str(r[1] + id_coord_start)]['x'],
                             'y_j': coord[str(r[1] + id_coord_start)]['y']})
        
        
        




            
