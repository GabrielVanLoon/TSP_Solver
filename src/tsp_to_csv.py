import csv
from math import ceil

def tsp_to_csv(tsp_filename, csv_filename):
    '''
    Transfere o id e as coordenadas do arquivo tsp para o arquivo csv

    Parametros
    ----------
        tsp_filename : str
            Nome do arquivo tsp em que sera retirada a informacao
            Estes arquivos estao localizados na pasta '/data/raw'
        csv_filename : str
            Nome do arquivo csv com cabecalho (id, x, y) sendo
            id o indice da localizacao, x a latitude e y a 
            longitude
            Eh recomendavel colocar o csv na pasta '/data/coord'

    Retorno
    -------
        True
            Foi possivel transferir os dados do arquivo tsp para o csv 
        False
            Nao foi possivel transferir os dados do tsp para o csv
    '''

    with open(tsp_filename, 'r', encoding='utf-8') as tsp_file:

        start_reference = 'NODE_COORD_SECTION\n'
        end_reference = 'EOF\n'
        reader = tsp_file.readlines()

        if start_reference not in reader:
            return False

        with open(csv_filename, 'w') as csv_file:

            writer = csv.DictWriter(csv_file, fieldnames=['id', 'x', 'y'])
            writer.writeheader()

            start = reader.index(start_reference) + 1
            if end_reference not in reader:
                end = len(reader)
            else:
                end = reader.index(end_reference)

            for row in reader[start:end]:
                line = row.strip().split()
                writer.writerow({'id': int(line[0]), 'x': ceil(float(line[1])), 'y': ceil(float(line[2]))})

        return True
