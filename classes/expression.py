# CNF expression class
from classes.clause import Clause
import numpy as np


# Class to represent a CNF expression
# Built as a collection of clause objects
# Supports symmetric difference between expressions
class Expression():

    def __init__(self, filename):
        self.clauses = self.read_cnf(filename)

    # Read a CNF expression from an external file, assuming the expression in
    # the file is written in the DIMACS CNF file format
    # (https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html)
    def read_cnf(self, filename):
        clauses = []

        file = open("cnffiles/" + filename).read().split("\n")

        for line in file:
            # Exclude lines that are comments or state the entire expression
            # definition
            if not (line[0] == "c" or line[0] == "p"):
                terms = [term for term in line.split(" ")[:-1] if term]

                clauses.append(Clause(terms))

        return clauses
    
    # Make an expression printable
    def __repr__(self) -> str:
        result = ""
        
        for clause in self.clauses:
            var = str(clause)

            result = result + var + " ∧ "

        return result[:-3]
    
    # Symmetric difference operator
    # Gives a list of clauses from self that do not appear in other, and vice
    # versa
    def __xor__(self, other):
        result = []

        left_outer = [x for x in self.clauses if x not in other.clauses]
        right_outer = [x for x in other.clauses if x not in self.clauses]

        return left_outer + right_outer
    

