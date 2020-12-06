"""
    Benchmark generate stats for the solvers
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../parser/'))

import time 
import functools
import helper as helper
import matplotlib.pyplot as plt
from models.classic_solver import ClassicSolver as cs
from models.cutting_plane  import CuttingPlane  as dfj
from models.mtz            import MTZSolver     as mtz
from models.lazy_cutting_plane import LazyCuttingPlane as dfj2
from models.dl import DLSolver as dl
from models.gg import GGSolver as gg
from models.routing_tsp import DefaultSolver as default
from load_results import load_results 
from store_results import store_results 
from make_route import route_csv
from plot_route import plot

NAME_FILES = 'qatar194'
EXTENSION = '.txt'

distPath = "../../data/distances/"
plotsPath = "../../benchmarks/images/"
resultsPath = "../../benchmarks/results/"
routesPath = "../../data/routes/"
coordPath = "../../data/coord/"
routesPath = "../../data/routes/"

@functools.lru_cache(None)
def benchmark(callback, inputs):
    "Run function on all the inputs; return pair of (average_time_taken, results)."
    t0           = time.clock()
    results      = [callback(x) for x in inputs]
    t1           = time.clock()
    average_time = (t1 - t0) / len(inputs)
    return (average_time, results)

# TODO: passar para segundos ou outra escala mais ...
# TODO: testas por instancia
def timeit(method):
    '''
        @Decorator timeit
        Retorna o tempo de excução da função
        Não modifica a função.
    '''

    def timed(*args, **kw):
        ts = time.time();
        result = method(*args, **kw);
        te = time.time();

        # Armazenar resultado
        if 'log_time' in kw and 'name' in kw:
            name = kw['name']
            kw['log_time'][name].append((te - ts));
        else:
            print("%r  %2.5f ms" % (method.__name__, (te - ts) / 1000));
        return result
    return timed

@timeit
def miller_method(test_data, **kwargs):
    my_solver = mtz(test_data)
    my_solver.solve()
    return round(my_solver.objective_value, 1)

@timeit
def dl_method(test_data, **kwargs):
    my_solver = dl(test_data)
    my_solver.solve()
    return round(my_solver.objective_value, 1)

@timeit
def lazy_cutting_planes(test_data, **kwargs):
    my_solver = dfj2(test_data)
    my_solver.solve()
    return round(my_solver.objective_value, 1)

@timeit 
def gg_method(test_data, **kwargs):
    my_solver = gg(test_data)
    my_solver.solve()
    return round(my_solver.objective_value)

def compare_models(filename_sample, filename_results, index_start=-1, index_end=-1, step=1, comment="No comments"):
    '''
        Compara os modelos implementados (tempo) x (n cidades)

        Parametros
            filename_sample: str
                nome do arquivo de teste
            
            filename_results: str
                nome do arquivo de resultados
            
            TODO: Must erase already calculate ones
            index_end: int 
                Posição de onde termina os pontos testados
                Se receber -1 começa de onde parou

            step: int
                Passo que acrescenta pontos do teste
    '''

    # cs_name = cs.__name__;
    mtz_name = mtz.__name__;
    # dfj_name = dfj.__name__;
    # dfj2_name = dfj2.__name__;
    dl_name = dl.__name__;
    gg_name = gg.__name__;
    # default_name = default.__name__;

    print(mtz_name + ' ' + ' ' + dl_name + ' ' + gg_name)

    # Valores horizontais
    x = []
    
    # Tempo gerado por execução
    logtime_data = {}

    # Tempo gerado por execução
    logvalue_data = {}

    # Results runtime
    try:
        # Load previous data
        x, logtime_data, logvalue_data = load_results(filename_results)

        # Index not specified, take last used
        if len(x):
            index_start = x[-1] + step
  
    except:
        # Index not specified, take first posible
        if(index_start == -1):
            index_start = 3

        x = []

        logtime_data = {
            mtz_name : [],
            dl_name: [],
            gg_name: [],
        }

        logvalue_data = {
            mtz_name : [],
            dl_name: [],
            gg_name: [],
        }
    
    # Load matrix
    test_data = helper.load_data(distPath + filename_sample)

    # If end not specied, run all tests
    if(index_end == -1 or index_end > len(test_data)):
        index_end = len(test_data)

    i = int(index_start)
    while(test_data != [] and i <= index_end):
        # Run methods
        logvalue_data[mtz_name].append(miller_method(test_data[:i][:i], name= mtz_name, log_time= logtime_data))
        logvalue_data[dl_name].append(dl_method(test_data[:i][:i], name= dl_name, log_time= logtime_data))
        logvalue_data[gg_name].append(gg_method(test_data[:i][:i], name= gg_name, log_time= logtime_data))
        
        # Load x (horizontal)
        x.append(i);
        i += step

    if(x == [] or logtime_data == {}):
        return

    store_results(filename_results, x, logtime_data, logvalue_data, comment)
    return x, logtime_data

def plot_time_execution(x, logtime_data, filename='default'):
    '''
        Generate a imagem of run time
    '''

    # Cria quadro
    fig = plt.figure(figsize=(10,4));
    ax = fig.add_subplot(111);

    # Plot execution time
    for key in logtime_data:
        print(logtime_data[key])
        ax.plot(x, logtime_data[key], label= key + " time",  linewidth=3.5);
        ax.scatter(x, logtime_data[key]);
    
    # legendas e axes
    ax.set(title="Tempo(s) de execução em função de N", xlabel="N", ylabel="Tempo(segundos)");
    ax.legend(loc="best", fontsize='large');

    plt.savefig(plotsPath + filename, transparent=False)

if __name__ == "__main__":
    
    i = 5
    logtime_data = {}
    x = []
    # while i < 15:
    #     compare_models('uruguay734.txt', 'uruuay734.txt', index_end=i, step=5, comment="Running all night for qatar!")
    #     i += 5 

    x, logtime_data = compare_models(NAME_FILES + EXTENSION, NAME_FILES + EXTENSION, index_start=194, index_end=194, step=1, comment="Running " + NAME_FILES)
    plot_time_execution(x=x, logtime_data=logtime_data, filename=NAME_FILES)