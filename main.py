#!/usr/bin/env python3
import optparse
import os
import os.path
import src.helper as helper

from ortools.linear_solver import pywraplp

from src.plot_route import plot

from src.parser.tsp_to_csv      import tsp_to_csv
from src.parser.coord_to_matrix import make_matrix_dist
from src.parser.make_route      import route_csv

from src.models.classic_solver import ClassicSolver
from src.models.cutting_plane  import CuttingPlane
from src.models.mtz            import MTZSolver

def checkFilenames(options, inputFlag=True, outputFlag=True):
    '''
    Checks if user passed the necessary filenames

    Parameters
    ----------
        options : optparse.Values
            Object that contains the 'str' names for
            input and output files.
        inputFlag : bool
            Set to True if the input filename is
            necessary.
        outputFlag : bool
            Set to True if the output filename is
            necessary.

    Return
    ------
        True
            The user has passed the necessary filename(s).
        Flase
            The user has not passed all necessary filenames.
    '''

    if (inputFlag) and (options.input == ""):
        return False
    if (outputFlag) and (options.output == ""):
        return False
    return True

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog [options] arg")
    parser.add_option("-i", "--in", dest="input",
        default="", type="string",
        help="specify input filename")
    parser.add_option("-o", "--out", dest="output", 
        default="", type="string", 
        help="specify output filename")
    parser.add_option("-s", "--solver", dest="solver", 
        default="", type="string", 
        help="specify solving method")
    parser.add_option("-C", "--coordinates", dest="coord", 
        default="", type="string", 
        help="specify coordinate filename")
    parser.add_option("-b", "--background", dest="background", 
        action="store_true", 
        help="use this flag to...")

(options, args) = parser.parse_args()

#Paths to open and create files
tspPath = "data/raw/"
csvPath = "data/coord/"
txtPath = "data/distances/"
routesPath = "data/routes/"
plotsPath = "images/plots/"

if len(args) != 1:
    parser.error("incorrect number of arguments")

#Converts a raw .tsp file into a coordinates .csv file
if args[0] == "tsp":
    #Checks if filenames are not empty strings (default value)
    if(not checkFilenames(options)):
        print("Both input and output filenames are necessary")

    #Checks if input file exists
    elif(not os.path.isfile(tspPath + options.input)):
        print("Input file does not exist.")

    else:
        if tsp_to_csv(tspPath + options.input, csvPath + options.output):
            print("Successfully converted raw data into coordinates:")
            print(csvPath + options.output)
        else:
            print("There was an error with the conversion")
    
#Converts a coordinates .csv file into a distances .txt file
elif args[0] == "dist":
    #Checks if filenames are not empty strings (default value)
    if(not checkFilenames(options)):
        print("Input and output filenames are necessary")

    #Checks if input file exists
    elif(not os.path.isfile(csvPath + options.input)):
        print("Input file does not exist.")

    else:
        make_matrix_dist(csvPath + options.input, txtPath + options.output)
        print("Successfully converted coordinates into distances:")
        print(txtPath + options.output)

#Solve problem with chosen method
#If no method is chosen, use classic_solver method
elif args[0] == "solve":
    #Checks if input filename is not an empty string
    if(not checkFilenames(options, outputFlag=False)):
        print("Input filename is necessary")

    #Checks if input file exists
    elif(not os.path.isfile(txtPath + options.input)):
        print("Input file does not exist.")
    
    #
    elif(options.output != "") and (not os.path.isfile(csvPath + options.coord)):
        print("Coordinate file does not exist")

    else:
        #Gets data from distances .txt file
        test_data = helper.load_data(txtPath + options.input)
        #print(test_data)

        if(options.solver == "dfj"):
            print("Trying to solve problem with Cutting Plane Method...")
            my_solver = CuttingPlane(test_data)
        elif(options.solver == "mtz"):
            print("Trying to solve problem with MTZ Solver Method...")
            my_solver = MTZSolver(test_data)
        else:
            print("Trying to solve problem with Classic Solver Method...")
            my_solver = ClassicSolver(test_data)
        my_solver.solve()

        if  my_solver.status == pywraplp.Solver.OPTIMAL:
            my_solver.resolve_final_path()

            print('A Solution was found')
            print('Objective value:', my_solver.objective_value)

            #Checks if filenames are not empty strings (default value)
            if (options.output == ""):
                print('Final Route Configuration: ', my_solver.final_path)
            else:
                route_csv(my_solver.final_path, csvPath + options.coord, routesPath + options.output)
                print("Final Route Configuration created at:")
                print(routesPath + options.output)
        
        else:
            print('No optiomal solution was found.')

elif(args[0] == "plot"):
    #Checks if filenames are not empty strings (default value)
    if(not checkFilenames(options)):
        print("Both input and output filenames are necessary")

    #Checks if input file exists
    elif(not os.path.isfile(routesPath + options.input)):
        print("Input file does not exist.")

    else:
        plot(routesPath + options.input, plotsPath + options.output, options.background)
        print("Plot created at:")
        print(plotsPath + options.output)

elif(args[0] == "all"):
    if(not checkFilenames(options, outputFlag=False)):
        print("Input filename is necessary")
    else:
        os.system("./main.py tsp -i {0}.tsp -o {0}.csv".format(options.input))
        os.system("./main.py dist -i {0}.csv -o {0}.txt".format(options.input))

        if(options.solver == "dfj"):
            os.system("./main.py solve -i {0}.txt -o {0}.csv -s dfj -C {0}.csv".format(options.input))
        elif(options.solver == "mtz"):
            os.system("./main.py solve -i {0}.txt -o {0}.csv -s mtz -C {0}.csv".format(options.input))
        else:
            os.system("./main.py solve -i {0}.txt -o {0}.csv -C {0}.csv".format(options.input))
        
        os.system("./main.py plot -i {0}.csv -o {0}.png".format(options.input))

else:
    print("Invalid argument")
