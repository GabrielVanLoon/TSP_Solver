from math import ceil

DIR = '../../benchmarks/results/'

def store_results(results_filename, x, logtime_data, logvalue_data, comment):
    '''
    Salva testes em benchmarks resultados
    
    Parametros
    ----------
        results_filename : str
            Nome do arquivo de resultados em que sera retirada a informacao
            Estes arquivos estao localizados na pasta '/data/raw'
        x : []
            Coordenadas x dos dados
        logtime_data : {'key': []}
            Resultados em segundos dos testes.
    Retorno
    -------
        True tudo ocorreu bem
        False a gravação falhou
        Throw error: leitura do arquivo, diretório não encontrado.

    '''
    with open(DIR + results_filename, 'w') as results_file:
        if x is None or len(x) is False or logtime_data is None or logvalue_data is None:
            return False 

        results_file.write(f'NAME: {results_filename}\n')
        results_file.write(f'COMMENT: {comment}\n')
        results_file.write(f'TYPE: txt\n')
        results_file.write(f'DIMENSION: 5\n')
        results_file.write(f'LAST_RUN: {x[-1]}\n')

        # Hotizontal values
        results_file.write(f'HORIZONTAL_SECTION:')
        for num in x:
            results_file.write(f' {num}')   
        results_file.write(f'\n')

        # Runtimes
        results_file.write(f'TIME_SECTION\n')
        for key in logtime_data:
            results_file.write(f'{key}:')
            for value in logtime_data[key]:
                results_file.write(f' {value}')
            results_file.write(f'\n')
        
        # values
        results_file.write(f'VALUES_SECTION\n')
        for key in logvalue_data:
            results_file.write(f'{key}:')
            for value in logvalue_data[key]:
                results_file.write(f' {value}')
            results_file.write(f'\n')
        return True

if __name__ == "__main__":
    logdata_to_results('libra6.txt', [1], {'mtz': [2]}, comment="Just test")
    exit(0)