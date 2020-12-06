import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import csv
from math import ceil
from models.classic_solver import ClassicSolver as cs
from models.cutting_plane  import CuttingPlane  as dfj
from models.mtz            import MTZSolver     as mtz
from models.lazy_cutting_plane import LazyCuttingPlane as dfj2
from models.dl import DLSolver as dl
from models.gg import GGSolver as gg
from models.routing_tsp import DefaultSolver as default

DIR = '../../benchmarks/results/'

def load_results(results_filename):
    '''
    Carrega o arquivo de resultados em  dicionarios

    Parametros
    ----------
        results_filename : str
            Nome do arquivo de resultados em que sera retirada a informacao
            Estes arquivos estao localizados na pasta '/data/raw'
    Retorno
    -------
        logdata : dicionario { mtz: [], dfj: []}
        logerror : dicionario { mtz: [], dfj: []}
            Carrega ultimos resultados em dicionarios

    '''

    # cs_name = cs.__name__;
    mtz_name = mtz.__name__;
    # dfj_name = dfj.__name__;
    # dfj2_name = dfj2.__name__;
    dl_name = dl.__name__;
    gg_name = gg.__name__;
    # default_name = default.__name__;

    # Tempo gerado por execução
    logtime_data = {
        gg_name: [],
        mtz_name : [],
        dl_name: [],
        # default_name: [],
    }

    # Tempo gerado por execução
    logvalue_data = {
        gg_name: [],
        mtz_name : [],
        dl_name: [],
        # default_name: [],
    }


    horizontal =  []

    with open(DIR + results_filename, 'r', encoding='utf-8') as results_file:
        time_reference = 'TIME_SECTION\n'
        value_reference = 'VALUES_SECTION\n'
        end_reference = 'EOF\n'

        reader = results_file.readlines()

        if time_reference not in reader:
            return False
    
        # Read dimension
        line_dim = 3; # line dimension
        read_dim = reader[line_dim][:-1].split(' ')
        dim = int(read_dim[1])

        # Read x values
        line_horizontal = 5
        read_horizontal = reader[line_horizontal][:-1].split(' ')
        horizontal = [int(x) for x in read_horizontal[1:]]

        # Read results runtime from start
        start = reader.index(time_reference) + 1
        end = start + dim
        for row in reader[start:end]:
            line = row.strip().split()
            logtime_data[line[0][:-1]] = [float(x) for x in line[1:] if x != '']

        start = reader.index(value_reference) + 1
        end = start + dim
        for row in reader[start:end]:
            line = row.strip().split()
            logvalue_data[line[0][:-1]] = [float(x) for x in line[1:] if x != '']

    return horizontal, logtime_data, logvalue_data

if __name__ == "__main__":
    results_to_logdata('../../benchmarks/results/libra6.txt')
    exit(0)