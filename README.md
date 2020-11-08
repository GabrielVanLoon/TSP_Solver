# Solucionador de TSP (Travelling Salesman)
Script python que soluciona o problema do caixeiro viajante (TSP) utilizando técnicas de modelagem e otimização linear.

![TSP na Constelação de Libra](https://i.imgur.com/ISHtT9Q.png)


## Instalação & Dependências
O projeto as possui as seguintes dependências:

- **Python v3.7.1** ou superior 
- **Google OR-Tools (para python):** biblioteca de otimização open-source;
- **matplotlib:** biblioteca utilizada para gerar o plot dos caminhos
- **optparser:** biblioteca utilitária para gerar o script principal `main.py`

A instalação pode ser feita manualmente utilizando o gerenciador de pacote `pip` ou `conda` ou utilizando o arquivo `requirements.txt` como o exemplo a seguir

```bash=
pip install requirements.txt
```

## Como Utilizar
O script `main.py` foi criado para ser utilizado como interface CLI (*Command Line Interface*) para todas as funcionalidades do projeto.

Para ser utilizado, basta realizar a instação e utilizar ele diretamente como executável (`./main.py action [args]`) ou da forma clássica (`python3 main.py action [args]`).

O primeiro argumento `action` define o tipo de rotina que se deseja executar e seus funcionamentos estão listados à seguir.

***Disclaimer:** o script `main.py` deve ser executado preferencialmente estando na pasta raíz, evite execuções do tipo `python3 path/to/main.py`.*


### Action tsp 
```bash=
./main.py tsp -i libra6.tsp -o libra6.csv
```
O comando acima lê o arquivo `data/raw/libra6.tsp`, que contém informações sobre o problema, e extrai as informações das coordenadas para o arquivo `data/coord/libra6.csv`.
    
### Action dist
```bash=
./main.py dist -i libra6.csv -o libra6.txt
```
O comando acima lê as coordenadas do arquivo `data/coord/libra6.csv` e gera um arquivo `data/distances/libra6.txt` que contém uma matriz de distâncias.
    
### Action solve
```bash=
./main.py solve -i libra6.txt
```
O comando acima lê o arquivo de distâncias `data/distances/libra6.txt` e resolve o problema utilizando o método clássico. Ao terminar, imprime a configuração final da rota na tela.

```bash=
./main.py solve -i libra6.txt -C libra6.csv -o libra6.csv
```
Análogo ao anterior mas também lê um arquivo de coordenadas `data/coord/libra6.csv` e ao finalizar gera um arquivo, `data/routes/libra6.csv`, que contém a informação da configuração final da rota.

```bash=
./main.py solve -i libra6.txt -s dfj
```
Esse comando resolve o problema utilizando o **método de Cutting Planes.** Ao terminar, imprime a configuração final da rota na tela.

```bash=
./main.py solve -i libra6.txt -s mtz
```
Esse comando resolve o problema utilizando o **método de MTZ.** Ao terminar, imprime a configuração final da rota na tela.

### Action plot
```bash=
./main.py plot -i libra6.tsp -o libra6.png
```
O comando acima lê o arquivo de rotas `data/routes/libra6.csv`, e a partir deste gera uma imagem `images/plot/libra6.png` que ilustra o menor caminho encontrado.

### Action all
```bash=
./main.py all -i libra6 -s mtz
```

Lê o arquivo `data/raw/libra6.tsp` e executa todas as actions anteriores (tsp, dist, solve, plot) resolvendo o sistema com o modelo definido pela flag `-s` e gerando SEMPRE uma imagem do ciclo final encontrado.

## Autores
[Alberto Campos Neves](https://github.com/AlbertWolf99)

[Gabriel Van Loon](https://github.com/GabrielVanLoon) 

[João Ricardo Minoru Nagasava](https://github.com/JNagasava) 

[Mathias Fernandes Duarte Coelho](https://github.com/Math-O5) 

*Desenvolvido para a disciplina SME0110 - Programação Matemática (2020).*
