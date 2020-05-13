#!/usr/bin/python3

import sys, getopt
import random
import math
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
# num_hours_i_spent_on_this_assignment = more than 50
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
"""

"""
#####################################################
#####################################################

def main(argv):
   inputfile = ''
   N=0
   try:
      opts, args = getopt.getopt(argv,"hn:i:",["N=","ifile="])
   except getopt.GetoptError:
      print ('sudoku.py -n <size of Sodoku> -i <inputputfile>')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('sudoku.py  -n <size of Sodoku> -i <inputputfile>')
           sys.exit()
       elif opt in ("-n", "--N"):
           N = int(arg)
       elif opt in ("-i", "--ifile"):
           inputfile = arg
   instance = readInstance(N, inputfile)
   toCNF(N,instance,inputfile+str(N)+".cnf")




def readInstance (N, inputfile):
    if inputfile == '':
        return [[0 for j in range(N)] for i in range(N)]
    with open(inputfile, "r") as input_file:
        instance =[]
        for line in input_file:
            number_strings = line.split() # Split the line on runs of whitespace
            numbers = [int(n) for n in number_strings] # Convert to integers
            if len(numbers) == N:
                instance.append(numbers) # Add the "row" to your list.
            else:
                print("Invalid Sudoku instance!")
                sys.exit(3)
        return instance # a 2d list: [[1, 3, 4], [5, 5, 6]]


""" Question 1 """
def toCNF (N, instance, outputfile):
    """ Constructs the CNF formula C in Dimacs format from a sudoku grid."""
    """ OUTPUT: Write Dimacs CNF to output_file """
    output_file = open(outputfile, "w")
    "*** YOUR CODE HERE ***"
    
    def getIndex(x,y, N):
        return x + N * y
    
    def toBase(x,y,m,N):
        return (N * N * (x-1) + N * (y-1) + (m-1) + 1)
    
    dimacs = ""
    test = ""
    for i in range(N):
        for j in range(N):
            test = test + str((instance[i][j]))
    board = []
    clauses = 0
    
    #Board Requirements
    for i in range(N):
       for j in range(N):
            index = getIndex(i,j,N)
            val = test[index]
            if val != '0':
                val = int(toBase(i+1,j+1,int(val),N))
                dimacs = dimacs + str(val) + " 0" + "\n"
                clauses += 1

    for x in range(1, N+1):
        for y in range(1, N+1):
            di = ""
            for m in range(1, N+1):
                val1 = (toBase(x,y,m,N))
                di = di + (str(val1) + " ")
                clauses += 1
            dimacs = dimacs + di + "0" + "\n"

    row1 = []
    for x in range(1, N+1):
        for y in range(1, N+1):
            for m in range(1, N+1):
                for y1 in range(y+1, N+1):
                    val1 = toBase(x,y,m,N)
                    val2 = toBase(x,y1,m,N)
                    row1.append("-" + str(val1))
                    row1.append(" -" + str(val2) + " 0" + "\n")
                    clauses += 1
    dimacs = dimacs + ("".join(str(v) for v in row1))

    col1 = []
    for x in range(1,N+1):
        for y in range(1,N+1):
            for m in range(1,N+1):
                for x1 in range(x+1,N+1):
                    val1 = toBase(x,y,m,N)
                    val2 = toBase(x1,y,m,N)
                    col1.append("-" + str(val1))
                    col1.append(" -" + str(val2) + " 0" + "\n")
                    clauses += 1
    dimacs = dimacs + ("".join(str(v) for v in col1))

    mini1 = []
    root = int(math.sqrt(N))
    for i in range(1, N+1):
        for j in range(root):
            for m in range(root):
                for n in range(1,root+1):
                    for o in range(1, root):
                        for p in range(o+1, root+1):
                            val1 = toBase(root*j + n, root*m+o, i, N)
                            val2 = toBase(root*j + n, root*m+p, i, N)
                            mini1.append("-" + str(val1))
                            mini1.append(" -" + str(val2) + " 0" + "\n")
                            clauses += 1
    dimacs = dimacs + ("".join(str(v) for v in mini1))

    mini2 = []
    for k in range(1, N+1):
        for a in range(root):
            for b in range(root):
                for u in range(1, root):
                    for v in range(1, root+1):
                        for w in range(u+1, root+1):
                            for x in range(1, root+1):
                                val1 = toBase(root*a +u, root*b+v, k, N)
                                val2 = toBase(root*a +w, root*b+x, k, N)
                                mini2.append("-" + str(val1))
                                mini2.append(" -" + str(val2) + " 0" + "\n")
                                clauses += 1
    dimacs = dimacs + ("".join(str(v) for v in mini2))

    dimacs = "p cnf " + str(N*N*N) + " " + str(clauses) + "\n" + dimacs
    output_file.write(dimacs)

    "*** YOUR CODE ENDS HERE ***"
    output_file.close()




if __name__ == "__main__":
   main(sys.argv[1:])
