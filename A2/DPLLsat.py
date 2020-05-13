#!/usr/bin/python3

import sys, getopt
import itertools
import copy
import random
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass
    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if not (maxvar == self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
      # Variables are numbered from 1 to p
        for i in range(1,self.p+1):
            self.VARS.add(i)
    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s



def main(argv):
   inputfile = ''
   verbosity=False
   inputflag=False
   try:
      opts, args = getopt.getopt(argv,"hi:v",["ifile="])
   except getopt.GetoptError:
      print ('DPLLsat.py -i <inputCNFfile> [-v] ')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('DPLLsat.py -i <inputCNFfile> [-v]')
           sys.exit()
    ##-v sets the verbosity of informational output
    ## (set to true for output veriable assignments, defaults to false)
       elif opt == '-v':
           verbosity = True
       elif opt in ("-i", "--ifile"):
           inputfile = arg
           inputflag = True
   if inputflag:
       instance = SatInstance()
       instance.from_file(inputfile)
       solve_dpll(instance, verbosity)
   else:
       print("You must have an input file!")
       print ('DPLLsat.py -i <inputCNFfile> [-v]')


""" Question 2 """
# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#    list of false literals (if verbosity == True)
#
#  You will need to define your own
#  solve(VARS, F), pure-elim(F), propagate-units(F), and
#  any other auxiliary functions

def pickX(formula):
    used = []
    ran = random.choice(formula)
    used.append(ran)
    if len(used) > 1:
        if ran in used:
            ran = random.choice(formula)
    return ran

def unit_propagation(formula,vars):
    unit_clauses = []
    for c in formula:
        if len(c) == 1:
            for i in c:
                if i not in unit_clauses and -i not in unit_clauses:
                    unit_clauses.append(i)

    if len(unit_clauses) == len(vars):
        return formula, unit_clauses
   
    for i in unit_clauses:
        for l in formula:
            if len(l) > 1:
                if i in l:
                    formula.remove(l)
    
                if -i in l:
                    for l2 in l:
                        if (l2 == (-i)):
                            l.remove(-i)
            if len(l) == 1:
                if -i in l:
                    formula =-1
                    return formula, unit_clauses

    return(formula,unit_clauses)

def pure_elim(formula):
    assignment = []
    pures = []
    literals = []
    pure = []
    if formula == -1:
        return formula
    else:
        for clause in formula:
            for literal in clause:
                literals.append(literal)
        for literal in literals:
            if -literal not in literals:
                pures.append(literal)
        for i in pures:
            if i not in pure and -i not in pure:
                pure.append(i)
        for i in range(len(pure)):
            for clauses in formula:
                if pure[i] in clauses:
                    formula.remove(clauses)
        for i in range(len(pure)):
           formula.append([pure[i]])
    return(formula)


def solve(VARS, F):
    varsList=list(VARS)
    assignment = []
    F, unit_clauses= unit_propagation(F, varsList)
    F = pure_elim(F)
    if F == -1:
        return []
    if [] in F:
        return []
    if (len(F) == len(varsList)):
        for i in range(len(F)):
            if len(F[i]) == 1:
                assignment.append(F[i])
            else:
                assignment.clear()
                break

    for i in varsList:
        for j in F:
            if len(j) == 1:
                if i in j:
                    if -i in j:
                        c = [x for x in j if x != -i]
                        if len(c) == 0:
                            F = []
                            return F
    variables = []
    if len(assignment) != len(varsList):
        for i in range(len(varsList)):
            if i < len(varsList):
                x = pickX(varsList)
                break
            else:
                F = F

    if len(assignment) == len(varsList) or len(unit_clauses) == len(varsList):
        return F
    elif solve(VARS,copy.deepcopy(F + [[x]])) !=[]:
        return solve(VARS, copy.deepcopy(F + [[x]]))
    else:
        return solve(VARS, copy.deepcopy(F + [[-x]]))


def solve_dpll(instance, verbosity):
    #print(instance)
    #print(instance.VARS)
    #print(verbosity)
    ###########################################
    # Start your code
    clauses = solve(instance.VARS,instance.clauses)
    test = []
    for clause in clauses:
        for i in clause:
            test.append(i)
    true = []
    false = []
    if clauses:
        print("SAT")
        if verbosity:
            for i in test:
                if i > 0:
                    true.append(i)
                else:
                    false.append(i)
            print("list of true literals:" + str(true))
            print("list of False literals:" + str(false))
    else:
        print("UNSAT")
    # End your code
    return True
    ###########################################


if __name__ == "__main__":
   main(sys.argv[1:])
