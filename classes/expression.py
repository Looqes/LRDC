# CNF expression class
from classes.clause import Clause
import numpy as np


# Class to represent a CNF expression
# Built as a collection of clause objects
# Supports symmetric difference between expressions
class Expression():
    # Constructor supports input of set of clauses to build expression.
    # Empty if none are given, to read from file call read function afterwards.
    def __init__(self, clauses=[]):
        # klaus
        self.clauses = clauses
        self.amount_of_literals = sum([clause.length for clause in self.clauses])


    # Read a CNF expression from an external file, assuming the expression in
    # the file is written in the DIMACS CNF file format
    # (https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html)
    def read_from_file(self, filename):
        clauses = []

        file = open("cnffiles/" + filename).read().split("\n")

        for line in file:
            # Exclude lines that are comments or state the entire expression
            # definition
            # print(line)
            if not (line[0] == "c" or line[0] == "p"):
                terms = [term for term in line.split(" ")[:-1] if term]
                # print(terms)
                clauses.append(Clause(terms))

        self.clauses = clauses
        self.amount_of_literals = sum([clause.length for clause in self.clauses])

        return self

    
    # Make an expression printable
    def __repr__(self) -> str:
        result = ""
        
        for clause in self.clauses:
            var = str(clause)

            result = result + var + " ∧ "

        return result[:-3]
    

    # Symmetric difference operator
    # Gives a list of clauses from self that do not appear in other, and vice
    # versa. The first step of the algorithm: "Full overlap removal"
    def __xor__(self, other):
        left_outer = [x for x in self.clauses if x not in other.clauses]
        right_outer = [x for x in other.clauses if x not in self.clauses]

        return Expression(left_outer), Expression(right_outer)
    

    # Function to extract clauses from an expression that share partial overlap
    # of literals with atleast one claus from the other expression, and vice versa
    def partial_overlap(self, other):
        result1 = set()
        result2 = set()

        for clause in self.clauses:
            for other_clause in other.clauses:
                print(clause)
                print(other_clause)
                test = clause & other_clause                
