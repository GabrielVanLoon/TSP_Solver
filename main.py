#!/usr/bin/env python3
import optparse
import os.path
from src.parser.tsp_to_csv import tsp_to_csv
from src.parser.coord_to_matrix import make_matrix_dist

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

(options, args) = parser.parse_args()

#Paths to open and create files
tspPath = "data/raw/"
csvPath = "data/coord/"
txtPath = "data/distances/"

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

else:
    print("Invalid argument")
