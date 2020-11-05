MAXN = 9999
dir = str('../../tests/')

def default_cast_value(value):
    return int(value)


def load_data(cast_value = default_cast_value):
    """
        Read a matrix of cost on the file .txt
        and load into matrix
    """
    # open and read file
    file = open(dir + '6.txt')
    lines = file.readlines()
    file.close()

    # Process file into matrix
    cost_matrix = []
    for i in range(len(lines)):
        aux = lines[i][:-1].split('\t')[0].split(' ')
        aux = [cast_value(i) for i in aux if (i != '')]
        cost_matrix.append(aux)

    return cost_matrix