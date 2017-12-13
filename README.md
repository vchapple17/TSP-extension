# Traveling Salesman Python & C
## Description
TSP is NP-Hard.  Included is a nearest neighbor algorithm with 2-Opt Swap.  A kd-tree structure is implemented to determine the nearest neighbor in Python 2.7, and the 2-Opt Swap is implemented in C.

## Usage
* Bash scripts
    * Each script corresponds to a file in the folder tsp_test_cases
    * scripts ending in a b are for the test-input files.
* main.py
    * Run with `python2.7 main.py python main.py ./tsp_test_cases/tsp_example_1.txt` for example 1 test file

## Files
* NN_KDTree
    * KDTree_main.py file that implements the kd-tree structure and 2-Opt swap
    * \_twoOpt.c and \_twoOpt.so python C-extension files copied from twoOpt folder
* tsp_test_cases
    * contains .txt files of 10 samples of city data.
        * Each line in the file contains a city ID, city x-coordinate and y-coordinate separated by spaces.
        * There is a corresponding script file to test each sample
    * Solutions to each file end in .tour
    * Time to get each solution end in .tourTime
* twoOpt
    * \_twoOpt.c - C-extension file
    * main.py - file to test C-extension
    * setup.py - build extension `python setup.py build_ext -i`
    * twoOpt.c and twoOpt.h - C function for 2-Opt Swap
* util (Supplementa)
    * tsp-verifier.py and TSPAllVisited.py
    * useful for that solutions are a valid solutions to the TSP problem.


## Results
TSP results with kd-tree in Python and 2-Opt in C

| File                | Num. Cities  | Min Dist | Time (sec)  |
| ------------------- |:------------:| :-------:|:-----------:|
| tsp_example_1.txt   | 76           | 118530   | 0.0105      |
| tsp_example_2.txt   | 280          | 3100     | 0.0640      |
| tsp_example_3.txt   | 15112        |          | |
| test-input-1.txt    | 50           | 5707     | 0.0064      |
| test-input-2.txt    | 100          | 8458     | 0.0122      |
| test-input-3.txt    | 250          | 14099    | 0.0509      |
| test-input-4.txt    | 500          | 19588    | 0.1494      |
| test-input-5.txt    | 1000         | 26301    | 0.8517      |
| test-input-6.txt    | 2000         | 36928    | 7.899       |
| test-input-7.txt    | 5000         | 57659    | 358.8       |
