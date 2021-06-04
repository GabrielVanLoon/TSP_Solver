#!/usr/bin/env python3
import os
import os.path

from tabulate import tabulate

resultPath = "../../data/log/"
bestknowPath = "../../data/raw/best_know.txt"

header1 = ['Instâncias', 'Tamanho', 'Melhor Sol.', 'DFJ', 'MTZ', '2opt',  'Chrs.']
header2 = ['Instâncias', 'DFJ Erro(%)', 'MTZ Erro(%)', '2opt Erro(%)', 'Chris. Erro(%)']
table1 = [header1]
table2 = [header2]

def read_heuristic(filename):
     # open and read file
    try:
        file = open(resultPath + filename)
        lines = file.readlines()
        file.close()
    except:
        return 0
    for line in lines:
        if "Objective value" in line:
            return float(line.strip().split(":")[-1])
    return -1

    
def read_exact(filename):

    # open and read file
    try:
        file = open(resultPath + filename)
        lines = file.readlines()
        file.close()
    except:
        return 0

    gap = 0.0
    for line in lines:
        if "Gap                :" in line:
            gap = line.strip().split(":")[-1]
        if "Objective value:" in line:
            return [float(line.strip().split(":")[-1]), gap]
    return [-1, -1]


# Load best know results
def load_bestknow(filename):
    '''
        Read a matrix of cost on the file .txt
        and load into dict
    '''
    # open and read file
    try:
        file = open(filename)
        lines = file.readlines()
        file.close()
    except:
        return []

    # Process file into dict
    dicio = dict()
    
    for line in lines:
        key, value  = line.strip().split(':')
        dicio[key.strip()] = float(value)

    return dicio

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def load_rows(dir):

    best_know = load_bestknow(bestknowPath)
    rows = []
    rows2 = []

    for root, dirs, files in os.walk("./../../data/log/"):
        dfj = 0
        mtz = 0
        opt = 0
        christofides = 0
        dfj_gap = "N/A"
        mtz_gap = "N/A"
        opt_gap = "N/A"
        christofides_gap = "N/A"
        inst = 0
        
        for filename in files:
            name = filename.split('.')[0] # ignore extension
            instancia, method = name.split('_')

            if instancia not in best_know.keys():
                continue

            bw = best_know[instancia]

            if method == "dfj2":
                dfj, gap = read_exact(filename)
                if dfj != -1:
                    dfj_gap = gap
            elif method == "mtz":
                mtz, gap = read_exact(filename)
                if mtz != -1:
                    mtz_gap = gap
            elif method == "2opt":
                opt = read_heuristic(filename)
                if opt != -1:
                    opt_gap =  "%.3f" % round(((opt - bw) / bw), 3)*100 + "%" 
            elif method == "christofides":
                christofides = read_heuristic(filename)
                if christofides != -1:
                    christofides_gap = "%.3f" % round(((christofides - bw) / bw), 3)*100 + "%"

            inst += 1

            # add row and append
            if inst == 4:
                # add row
                inst_size = int(''.join(i for i in instancia if i.isdigit()))
                rows.append([instancia, inst_size, bw, dfj, mtz, opt, christofides])
                rows2.append([instancia, dfj_gap, mtz_gap, opt_gap, christofides_gap])

                # reset
                inst = 0
                dfj_gap = "N/A"
                mtz_gap = "N/A"
                opt_gap = "N/A"
                christofides_gap = "N/A"
    return [rows, rows2]

rows, rows2 = load_rows(resultPath)
for row in rows:
    table1.append(row)

for row in rows2:
    table2.append(row)

print(tabulate(table1, headers='firstrow', tablefmt='latex'))
print(tabulate(table2, headers='firstrow', tablefmt='latex'))