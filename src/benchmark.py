"""
    Benchmark generate stats for the solvers
"""
import time 
import functools
import helper as helper
import matplotlib.pyplot as plt
from models.classic_solver import ClassicSolver as cs
from models.cutting_plane  import CuttingPlane  as dfj
from models.mtz            import MTZSolver     as mtz
from models.lazy_cutting_plane import LazyCuttingPlane as dfj2


distPath = "data/distances/"
plotsPath = "benchmarks/images/"

@functools.lru_cache(None)
def benchmark(callback, inputs):
    "Run function on all the inputs; return pair of (average_time_taken, results)."
    t0           = time.clock()
    results      = [callback(x) for x in inputs]
    t1           = time.clock()
    average_time = (t1 - t0) / len(inputs)
    return (average_time, results)

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
            kw['log_time'][name].append((te - ts) * 1000);
        else:
            print("%r  %2.5f ms" % (method.__name__, (te - ts) * 1000));
        return result
    return timed

@timeit
def classic_solver(test_data, **kwargs):
    my_solver = cs(test_data)
    my_solver.solve()
    # print( my_solver.objective_value)
    return my_solver.objective_value

@timeit
def cutting_planes(test_data, **kwargs):
    my_solver = dfj(test_data)
    my_solver.init_constraints()
    my_solver.solve()
    # print( my_solver.objective_value)
    return my_solver.objective_value

@timeit
def miller_method(test_data, **kwargs):
    my_solver = mtz(test_data)
    my_solver.solve()
    # print( my_solver.objective_value)
    return my_solver.objective_value

@timeit
def lazy_cutting_planes(test_data, **kwargs):
    my_solver = dfj2(test_data)
    my_solver.solve()
    max_cycles = 100
    i = 0
    while(i < max_cycles):
        # print('The problem does not have an optimal solution in cycle: %d' %(i))
        # print("The upper bound solution is %d " % (my_solver.objective_value))
        if(my_solver.block_subpath() is True):
            my_solver.solve()
        else:
            break
        i += 1 
    return my_solver.objective_value

def compare_models():
    '''
        Compara os modelos implementados (tempo) x (n cidades)
    '''
    
    cs_name = cs.__name__;
    mtz_name = mtz.__name__;
    dfj_name = dfj.__name__;
    dfj2_name = dfj2.__name__;
    print(cs_name + ' ' + ' ' + dfj_name + ' ' + mtz_name + ' ' + dfj2_name)

    # Tempo gerado por execução
    logtime_data = {
        cs_name : [],
        dfj2_name : [],
        mtz_name : [],
        dfj_name : [],
    }

    # Read file from 3 to n.txt
    i = 3
    x = []
    test_data = helper.load_data(distPath + str(i) + '.txt')
    while(test_data != [] and i < 11):
        # Run methods
        classic_solver(test_data, name= cs_name, log_time= logtime_data)
        cutting_planes(test_data, name= dfj_name, log_time= logtime_data)
        lazy_cutting_planes(test_data, name= dfj2_name, log_time= logtime_data)
        miller_method(test_data, name= mtz_name, log_time= logtime_data)

        # Load dara
        x.append(i);
        i += 1
        test_data = helper.load_data(distPath + str(i) + '.txt')
    return [x, logtime_data]

def plot_time_execution(x, logtime_data, filename='default'):
    '''
        Generate a imagem of run time
    '''

    # Cria quadro
    fig = plt.figure(figsize=(10,4));
    ax = fig.add_subplot(111);

    # Plot execution time
    for key in logtime_data:
        ax.plot(x, logtime_data[key], label= key + " time",  linewidth=3.5);
        ax.scatter(x, logtime_data[key]);
    
    # legendas e axes
    ax.set(title="Tempo(s) de execução em função de N", xlabel="N", ylabel="Tempo(milesegundos)");
    ax.legend(loc="best", fontsize='large');

    plt.savefig(plotsPath + filename, transparent=False)

x, logtime_data = compare_models()
plot_time_execution(x=x, logtime_data=logtime_data, filename='2')