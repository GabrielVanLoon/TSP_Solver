import matplotlib.pyplot as plt

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

FILE_NAMES = ['qatar194_dl.out', 'qatar194_mtz.out']
def plot_solution():
