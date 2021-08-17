dir = str('./')

def load_data(filename):
    '''
        Read a matrix of cost on the file .txt
        and load into matrix
    '''
    # open and read file
    try:
        print(dir + filename)
        file = open(dir + filename)
        lines = file.readlines()
        file.close()
    except:
        return []

    # Process file into matrix
    cost_matrix = list()
    
    for line in lines:
        cost_matrix.append([float(x) for x in line.strip().split('\t')])

    return cost_matrix