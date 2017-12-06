#!/usr/bin/python2.7

# Val Chapple
# Cody Dhein
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
sys.path.append('./util')
sys.path.append('./MST')
sys.path.append('./NN_KDTree')

import timeit
from tsp_utils import Map, City
from MST import MST
from KDTree_main import kdTreeNN
import math
import random as rand

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

    # print 'File loaded with ' + str(inputSize)

    t2 = timeit.default_timer()

    if inputSize > 500:
        #print 'Run with KDTree'
        kdTreeNN( dataIn, outfilename)

        t3 = timeit.default_timer()

        # t3 - t2 is time taken to build the MST and route
        # print 'Finished kd-tree and route build, time: ' + str(t3-t2)

        exit(0)
    else: # Running with MST
        # Create data structure
        map = Map(dataIn)

        # determine starting node/city based on input size
        options = {50 : 10,
                76 : 2,
                280 : 43,
                100 : 43,
                250 : 174,
                500 : 42}

        startCity = options[inputSize]

        # Build MST and route
        mst = MST(map)
        mst.buildRoute(startCity)


        # Optimize route
        if inputSize == 250:
            mst.twoOptFI()
        else:
            mst.twoOptBI()

        length = mst.calcLength()
        t3 = timeit.default_timer()

        # t3 - t2 is time taken to build the MST and route
        # print 'Finished MST and route build, time: ' + str(t3-t2)

        fileWrite = open(outfilename, "w")
        mst.saveSolution(fileWrite)
        fileWrite.close()
        exit(0)
