#!/usr/bin/env python3
import os
import os.path
import optparse
import src.helper as helper

from ortools.linear_solver import pywraplp

from src.plot_route import plot

from src.parser.tsp_to_csv      import tsp_to_csv
from src.parser.coord_to_matrix import make_matrix_dist
from src.parser.make_route      import route_csv

from src.models.classic_solver import ClassicSolver
from src.models.cutting_plane  import CuttingPlane
from src.models.mtz            import MTZSolver
from src.models.lazy_cutting_plane import LazyCuttingPlane
from src.models.dl import DLSolver
from src.models.gg import GGSolver

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
rawPath = "data/raw/"
coordPath = "data/coord/"
distPath = "data/distances/"
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
    elif(not os.path.isfile(rawPath + options.input)):
        print("Input file does not exist.")

    else:
        if tsp_to_csv(rawPath + options.input, coordPath + options.output):
            print("Coordinates file successfully created at:")
            print(coordPath + options.output)
        else:
            print("There was an error with the conversion")
    
#Converts a coordinates .csv file into a distances .txt file
elif args[0] == "dist":
    #Checks if filenames are not empty strings (default value)
    if(not checkFilenames(options)):
        print("Input and output filenames are necessary")

    #Checks if input file exists
    elif(not os.path.isfile(coordPath + options.input)):
        print("Input file does not exist.")

    else:
        make_matrix_dist(coordPath + options.input, distPath + options.output)
        print("Distances file successfully created at:")
        print(distPath + options.output)

#Solve problem with chosen method
#If no method is chosen, use classic_solver method
elif args[0] == "solve":
    #Checks if input filename is not an empty string
    if(not checkFilenames(options, outputFlag=False)):
        print("Input filename is necessary")

    #Checks if input file exists
    elif(not os.path.isfile(distPath + options.input)):
        print("Input file does not exist.")
    
    #Checks if coordinates file exists
    elif(options.output != "") and (not os.path.isfile(coordPath + options.coord)):
        print("Coordinate file does not exist")

    else:
        #Gets data from distances .txt file
        test_data = helper.load_data(distPath + options.input)

        #Checks chosen solving method
        if(options.solver == "dfj"):
            print("Trying to solve problem with Cutting Plane Method...")
            my_solver = CuttingPlane(test_data)
        elif(options.solver == "mtz"):
            print("Trying to solve problem with MTZ Solver Method...")
            my_solver = MTZSolver(test_data)
        elif(options.solver == "dfj2"):
            print("Trying to solve problem with DFJ version 2.0 Method...")
            my_solver = LazyCuttingPlane(test_data)
        elif(options.solver == "dl"):
            print("Trying to solve problem with DL version Method...")
            my_solver = DLSolver(test_data)
        elif(options.solver == "gg"):
            print("Trying to solve problem with GG version Method...")
            my_solver = GGSolver(test_data)
        else:
            print("Trying to solve problem with Classic Solver Method...")
            my_solver = ClassicSolver(test_data)
        my_solver.solve()

        if  my_solver.status == pywraplp.Solver.OPTIMAL:            
            my_solver.resolve_final_path()

            print('A Solution was found')
            print('Objective value:', round(my_solver.objective_value, 1))

            #Checks if output filename is empty
            #If it is, simply prints the final route
            if (options.output == ""):
                print('Final Route Configuration: ', my_solver.final_path)

            #If there is an output filename
            #Creates a route .csv file
            else:
                route_csv(my_solver.final_path, coordPath + options.coord, routesPath + options.output)
                print("Final Route Configuration succesfully created at:")
                print(routesPath + options.output)
        
        elif my_solver.status == pywraplp.Solver.FEASIBLE:
            if  my_solver.status == pywraplp.Solver.OPTIMAL:            
                my_solver.resolve_final_path()

                print('An aproximation Solution was found')
                print('Objective value:', round(my_solver.objective_value, 1))

            #Checks if output filename is empty
            #If it is, simply prints the final route
                if (options.output == ""):
                    print('Final Route Configuration: ', my_solver.final_path)
        else:
            print('No optiomal solution was found.')

#Plots the found solution
elif(args[0] == "plot"):
    #Checks if filenames are not empty strings (default value)
    if(not checkFilenames(options)):
        print("Both input and output filenames are necessary")

    #Checks if input file exists
    elif(not os.path.isfile(routesPath + options.input)):
        print("Input file does not exist.")

    else:
        plot(routesPath + options.input, plotsPath + options.output, options.background)
        print("Plot image successfully created at:")
        print(plotsPath + options.output)

#Executes in order the commands needed to solve and plot
#the solution of the problem with just the raw file
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
        elif(options.solver == "dfj2"):
            os.system("./main.py solve -i {0}.txt -o {0}.csv -s dfj2 -C {0}.csv".format(options.input))
        else:
            os.system("./main.py solve -i {0}.txt -o {0}.csv -C {0}.csv".format(options.input))
        
        os.system("./main.py plot -i {0}.csv -o {0}.png".format(options.input))

else:
    print("Invalid argument")
