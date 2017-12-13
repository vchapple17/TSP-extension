#!/usr/bin/python2.7

# C-Extensions: Val Chapple
# Modified Dec 6, 2017

# Amended from
# Val Chapple and Cody Dhein
# Date: Nov 30, 2017

# TSP Driver program
# Reads input data set and selects algorithm based on size.
#
# Usage:
# python2.7 main.py <filename>
# INPUTS:
# filename:
#   contains filename of a text file that has each line as a city with city Id, x-coord, y-coord

import sys
import os.path
sys.path.append('./NN_KDTree')

import timeit
from KDTree_main import kdTreeNN

if __name__ == '__main__':
    # Check input file name exists and is readable file
    try:
        filename = sys.argv[1]
    except:
        print("Usage: " + sys.argv[0] + " [options]" + " <inputfilename>")
        sys.exit()

    try:
        inFile = open(filename, "r")
    except:
        print("No file named: " + filename)
        sys.exit()

   # Split text input into lines and read length to determine algorithm to run
    dataIn = inFile.read().splitlines()
    inputSize = len(dataIn)
    outfilename = filename + ".tour"

    t2 = timeit.default_timer()

    kdTreeNN( dataIn, outfilename)

    t3 = timeit.default_timer()
    print("time: " + str(t3-t2))
    # Save time
    outFile = open(outfilename + "Time", "w")
    outFile.write(str(t3-t2) + "\n")
    outFile.close()
