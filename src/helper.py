dir = str('./')

def load_data(filename):
    """
        Read a matrix of cost on the file .txt
        and load into matrix
    """
    # open and read file
    file = open(dir + filename)
    lines = file.readlines()
    file.close()

    # Process file into matrix
    cost_matrix = list()
    
    for line in lines:
        # print(line.split())
        cost_matrix.append([int(x) for x in line.strip().split('\t')])

    #for i in range(len(lines)):
    #    aux = lines[i][:-1].split('\t')[0].split(' ')
    #    aux = [i for i in aux if (i != '')]
    #    cost_matrix.append(aux)

    return cost_matrix